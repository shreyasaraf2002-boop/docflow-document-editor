const $ = id => document.getElementById(id);
let activeId = null, saveTimer = null, loading = false, selectedUser = '1';
const userId = () => selectedUser;
const api = async (path, options={}) => {
  const headers = {'X-User-Id':userId(), ...(options.headers||{})};
  if (options.body && !(options.body instanceof FormData)) headers['Content-Type']='application/json';
  const response = await fetch('/api'+path, {...options,headers});
  let data; try { data=await response.json(); } catch { throw Error('Unexpected server response'); }
  if (!response.ok) throw Error(data.error||'Request failed');
  return data;
};
function toast(message){$('toast').textContent=message;$('toast').hidden=false;setTimeout(()=>$('toast').hidden=true,3000)}
function status(message){$('status').textContent=message}
function clearEditor(){activeId=null;$('workspace').hidden=true;$('empty').hidden=false}
async function refreshList(){
  const docs=await api('/documents');
  $('documents').replaceChildren();
  if(!docs.length){const p=document.createElement('p');p.style.cssText='padding:10px;color:#9ba6b8;font-size:12px';p.textContent='No documents yet';$('documents').append(p)}
  for(const d of docs){
    const card=document.createElement('div');card.className='doc-item'+(d.id===activeId?' selected':'');
    const icon=document.createElement('span');icon.className='icon';icon.textContent='▤';
    const description=document.createElement('div');const title=document.createElement('div');title.className='doc-name';title.textContent=d.title;
    const meta=document.createElement('small');meta.textContent=d.access==='owned'?'Mine':'Shared by '+d.owner_name;
    description.append(title,meta);card.append(icon,description);card.onclick=()=>openDoc(d.id);$('documents').append(card);
  }
}
async function openDoc(id){
  if(activeId!==null && activeId!==id) await save(true);
  const doc=await api('/documents/'+id);loading=true;activeId=id;
  $('title').value=doc.title;$('editor').innerHTML=doc.content;
  $('empty').hidden=true;$('workspace').hidden=false;
  status('All changes saved');loading=false;await refreshList();
}
async function createDoc(){try{if(activeId!==null)await save(true);let d=await api('/documents',{method:'POST',body:JSON.stringify({title:'Untitled Document'})});await openDoc(d.id);$('title').focus();$('title').select()}catch(e){toast(e.message)}}
async function save(silent=false){
  if(activeId===null||loading)return;
  clearTimeout(saveTimer);const id=activeId;status('Saving…');
  try{await api('/documents/'+id,{method:'PUT',body:JSON.stringify({title:$('title').value||'Untitled Document',content:$('editor').innerHTML})});if(activeId===id)status('All changes saved');if(!silent){await refreshList();toast('Document saved')}}catch(e){status('Save failed');toast(e.message)}
}
function scheduleSave(){if(loading||activeId===null)return;status('Unsaved changes');clearTimeout(saveTimer);saveTimer=setTimeout(()=>save(true),750)}
$('new').onclick=createDoc;$('empty-new').onclick=createDoc;
$('title').addEventListener('input',scheduleSave);$('editor').addEventListener('input',scheduleSave);
$('save').onclick=()=>save();
$('toolbar').addEventListener('mousedown',e=>{if(e.target.closest('button'))e.preventDefault()});
$('toolbar').addEventListener('click',e=>{const button=e.target.closest('button[data-cmd]');if(!button)return;$('editor').focus();document.execCommand(button.dataset.cmd,false,button.dataset.val||null);scheduleSave()});
$('file').addEventListener('change',async e=>{
 const f=e.target.files[0];if(!f)return;
 try{if(activeId!==null)await save(true);const form=new FormData();form.append('file',f);const doc=await api('/upload',{method:'POST',body:form});await openDoc(doc.id);toast('File imported successfully')}catch(err){toast(err.message)}finally{e.target.value=''}
});
$('share').onclick=async()=>{try{const doc=await api('/documents/'+activeId);if(doc.owner_id!==Number(userId()))return toast('Only the owner can share this document');const users=await api('/users');$('recipient').replaceChildren();for(const u of users.filter(x=>x.id!==Number(userId()))){const opt=document.createElement('option');opt.value=u.id;opt.textContent=u.name;$('recipient').append(opt)}$('share-dialog').showModal()}catch(e){toast(e.message)}};
$('cancel-share').onclick=()=>$('share-dialog').close();
$('confirm-share').onclick=async()=>{try{await api('/documents/'+activeId+'/share',{method:'POST',body:JSON.stringify({user_id:Number($('recipient').value)})});$('share-dialog').close();toast('Document shared! Switch users to see it.')}catch(e){toast(e.message)}};
$('user').onchange=async()=>{try{if(activeId!==null)await save(true);selectedUser=$('user').value;clearEditor();await refreshList()}catch(e){toast(e.message)}};
window.addEventListener('beforeunload',()=>clearTimeout(saveTimer));
refreshList().catch(e=>toast(e.message));
