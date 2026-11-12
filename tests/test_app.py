import os
import tempfile
import pytest

@pytest.fixture
def client(monkeypatch):
    fd, path = tempfile.mkstemp(suffix='.db');os.close(fd)
    monkeypatch.setenv('DATABASE_PATH', path)
    import importlib
    import app as module
    importlib.reload(module)
    module.app.config['TESTING']=True
    with module.app.test_client() as c:
        yield c
    os.unlink(path)

def test_create_edit_share_and_persist(client):
    response=client.post('/api/documents',json={'title':'Example','content':'<h2>Hello</h2>'},headers={'X-User-Id':'1'})
    assert response.status_code==201
    doc_id=response.json['id']
    assert client.get(f'/api/documents/{doc_id}',headers={'X-User-Id':'2'}).status_code==404
    assert client.put(f'/api/documents/{doc_id}',json={'title':'Updated','content':'<b>Saved</b>'},headers={'X-User-Id':'1'}).status_code==200
    assert client.post(f'/api/documents/{doc_id}/share',json={'user_id':2},headers={'X-User-Id':'1'}).status_code==200
    shared=client.get(f'/api/documents/{doc_id}',headers={'X-User-Id':'2'})
    assert shared.status_code==200
    assert shared.json['title']=='Updated'
    assert shared.json['content']=='<b>Saved</b>'
    assert client.post(f'/api/documents/{doc_id}/share',json={'user_id':1},headers={'X-User-Id':'2'}).status_code==403

def test_upload_rejects_bad_extension(client):
    from io import BytesIO
    res=client.post('/api/upload',data={'file':(BytesIO(b'no'), 'malware.exe')},content_type='multipart/form-data')
    assert res.status_code==400
