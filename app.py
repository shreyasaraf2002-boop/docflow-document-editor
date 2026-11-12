import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request, g
from werkzeug.exceptions import HTTPException

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
DB = os.environ.get('DATABASE_PATH', str(BASE / 'docflow.db'))

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db

@app.teardown_appcontext
def close_db(exc):
    conn = g.pop('db', None)
    if conn is not None: conn.close()

def init_db():
    with app.app_context():
        db().executescript('''
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
        CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER NOT NULL REFERENCES users(id), title TEXT NOT NULL DEFAULT 'Untitled Document', content TEXT NOT NULL DEFAULT '', updated_at TEXT NOT NULL DEFAULT (datetime('now')));
        CREATE TABLE IF NOT EXISTS shares(doc_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE, user_id INTEGER NOT NULL REFERENCES users(id), PRIMARY KEY(doc_id,user_id));
        INSERT OR IGNORE INTO users(id,name) VALUES (1,'Alex'),(2,'Sam');
        ''')
        db().commit()

@app.before_request
def startup():
    if not getattr(app, '_initialized', False):
        init_db()
        app._initialized = True

def current_user():
    try: uid = int(request.headers.get('X-User-Id') or request.args.get('user') or 1)
    except (ValueError, TypeError): return None
    return uid if db().execute('SELECT id FROM users WHERE id=?',(uid,)).fetchone() else None

def document(doc_id, uid, owner_only=False):
    row = db().execute('SELECT d.* FROM documents d WHERE d.id=? AND (d.owner_id=? OR (?=0 AND EXISTS (SELECT 1 FROM shares s WHERE s.doc_id=d.id AND s.user_id=?)))', (doc_id,uid,int(owner_only),uid)).fetchone()
    return row

def fail(message, status=400): return jsonify(error=message),status

def owned_or_shared(doc_id, uid):
    row = document(doc_id,uid)
    if row is None: return None
    return row

@app.get('/')
def home(): return render_template('index.html')

@app.get('/api/users')
def users(): return jsonify([dict(r) for r in db().execute('SELECT * FROM users ORDER BY id')])

@app.get('/api/documents')
def list_docs():
    uid=current_user()
    if not uid: return fail('Invalid user', 401)
    rows=db().execute('''SELECT d.id,d.title,d.updated_at,d.owner_id, u.name AS owner_name,
       CASE WHEN d.owner_id=? THEN 'owned' ELSE 'shared' END AS access
       FROM documents d JOIN users u ON u.id=d.owner_id
       WHERE d.owner_id=? OR EXISTS (SELECT 1 FROM shares s WHERE s.doc_id=d.id AND s.user_id=?)
       ORDER BY d.updated_at DESC,d.id DESC''',(uid,uid,uid)).fetchall()
    return jsonify([dict(x) for x in rows])

@app.post('/api/documents')
def create_doc():
    uid=current_user()
    if not uid: return fail('Invalid user',401)
    payload=request.get_json(silent=True) or {}
    title=str(payload.get('title') or 'Untitled Document').strip()[:150]
    content=str(payload.get('content') or '')
    if len(content)>2_000_000: return fail('Document too large',413)
    cur=db().execute('INSERT INTO documents(owner_id,title,content) VALUES (?,?,?)',(uid,title,content))
    db().commit()
    return jsonify(id=cur.lastrowid),201

@app.get('/api/documents/<int:doc_id>')
def get_doc(doc_id):
    uid=current_user()
    if not uid: return fail('Invalid user',401)
    row=owned_or_shared(doc_id,uid)
    if not row: return fail('Document not found or access denied',404)
    return jsonify(dict(row))

@app.put('/api/documents/<int:doc_id>')
def update_doc(doc_id):
    uid=current_user()
    if not uid:return fail('Invalid user',401)
    row=owned_or_shared(doc_id,uid)
    if not row:return fail('Document not found or access denied',404)
    p=request.get_json(silent=True) or {}
    title=str(p.get('title',row['title'])).strip()[:150]
    content=str(p.get('content',row['content']))
    if not title:return fail('Title cannot be empty')
    if len(content)>2_000_000:return fail('Document too large',413)
    db().execute("UPDATE documents SET title=?,content=?,updated_at=datetime('now') WHERE id=?",(title,content,doc_id))
    db().commit()
    return jsonify(ok=True)

@app.post('/api/documents/<int:doc_id>/share')
def share_doc(doc_id):
    uid=current_user()
    if not uid:return fail('Invalid user',401)
    if not document(doc_id,uid,owner_only=True):return fail('Only the document owner can share',403)
    p=request.get_json(silent=True) or {}
    try: recipient=int(p.get('user_id'))
    except (ValueError,TypeError):return fail('Choose a valid user')
    if recipient==uid:return fail('You already own this document')
    if not db().execute('SELECT id FROM users WHERE id=?',(recipient,)).fetchone():return fail('User not found',404)
    db().execute('INSERT OR IGNORE INTO shares(doc_id,user_id) VALUES (?,?)',(doc_id,recipient))
    db().commit()
    return jsonify(ok=True)

@app.post('/api/upload')
def upload():
    uid=current_user()
    if not uid:return fail('Invalid user',401)
    f=request.files.get('file')
    if not f or not f.filename:return fail('Select a file')
    ext=Path(f.filename).suffix.lower()
    if ext not in ('.txt','.md'):return fail('Only .txt and .md files are supported')
    try: content=f.read(1024*1024+1).decode('utf-8')
    except UnicodeDecodeError:return fail('File must use UTF-8 text encoding')
    if len(content.encode('utf-8'))>1024*1024:return fail('File too large (maximum 1 MB)',413)
    import html
    safe=html.escape(content)
    safe='<p>'+safe.replace('\n','<br>')+'</p>'
    title=Path(f.filename).stem[:150] or 'Imported document'
    cur=db().execute('INSERT INTO documents(owner_id,title,content) VALUES (?,?,?)',(uid,title,safe))
    db().commit()
    return jsonify(id=cur.lastrowid),201

@app.get('/health')
def health():return jsonify(status='ok')

@app.errorhandler(413)
def too_large(e):return fail('File too large (maximum 1 MB)',413)

if __name__=='__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG')=='1',host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
