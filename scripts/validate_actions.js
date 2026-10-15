// Validate the actual HTML data load order, every local asset, and original category preservation.
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const hash=value=>crypto.createHash('sha256').update(value).digest('hex');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const ctx={window:{},Set};vm.createContext(ctx);
for(const match of html.matchAll(/<script[^>]+src="(data\/[^"]+)"/g)){
  const file=match[1].split('?')[0];vm.runInContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
}
const M=ctx.window.MABI,errors=[];
const assert=(ok,message)=>{if(!ok)errors.push(message)};
const manifest=JSON.parse(fs.readFileSync(path.join(root,'GIF_MANIFEST.json'),'utf8'));
const baseline=JSON.parse(fs.readFileSync(path.join(root,'research/actions/baseline.json'),'utf8'));
for(const [file,sha] of Object.entries(baseline.original_files)){
  assert(fs.existsSync(path.join(root,file)),`Original file deleted: ${file}`);
  if(fs.existsSync(path.join(root,file)))assert(hash(fs.readFileSync(path.join(root,file)))===sha,`Original file changed: ${file}`);
}
assert(hash(JSON.stringify(M.DATA.filter(i=>i.type!=='action')))===baseline.data_sha256,'Existing appearance records changed');
assert(hash(JSON.stringify([M.PET_STATS,M.PET_FAMILY_BY_KO,M.PET_SKILL_FAMILIES]))===baseline.pet_data_sha256,'Pet information changed');
assert(hash(JSON.stringify([[...M.TW_CURRENT_IDS],[...M.TW_RELEASED_IDS],M.TW_STATUS_UPDATED]))===baseline.tw_sets_sha256,'Existing Taiwan status sets changed');
assert(new Set(M.DATA.map(i=>i.id)).size===M.DATA.length,'Duplicate record IDs');
assert(M.ACTION_BOXES.length===14,'Expected 14 action boxes');
assert(M.ACTION_BOXES.reduce((n,b)=>n+b.actions.length,0)===44,'Expected 44 actions');
const manifestByPath=new Map(manifest.files.map(f=>[f.relative_path,f]));
const used=new Set();
for(const [index,box] of M.ACTION_BOXES.entries()){
  assert(box.number===index+1,`Bad sequence: ${box.id}`);
  assert(index===0 || box.date>=M.ACTION_BOXES[index-1].date,`Bad chronology: ${box.id}`);
  assert(box.twReleased===true || box.twReleased===null,`Unverified Taiwan status must be null: ${box.id}`);
  for(const action of box.actions){
    assert(action.zh&&action.ko&&action.previews.length,`Missing action content: ${box.id}`);
    for(const preview of action.previews){
      assert(!/^https?:/.test(preview.path),`Remote playback URL: ${preview.path}`);
      const record=manifestByPath.get(preview.path);
      assert(record&&record.status==='success',`Not verified: ${preview.path}`);
      assert(record?.action_names_ko.includes(action.ko),`Action/GIF mismatch: ${box.id}/${action.ko}`);
      assert(record?.source_url===preview.sourceUrl,`Original source mismatch: ${preview.path}`);
      assert(fs.existsSync(path.join(root,preview.cover)),`Missing cover: ${preview.cover}`);
      used.add(preview.path);
    }
  }
}
for(const record of manifest.files){
  const file=path.join(root,record.relative_path);
  assert(fs.existsSync(file),`Missing GIF: ${record.relative_path}`);
  if(fs.existsSync(file)){
    const raw=fs.readFileSync(file);
    assert(['GIF87a','GIF89a'].includes(raw.subarray(0,6).toString()),`Invalid GIF signature: ${record.relative_path}`);
    assert(raw.length===record.bytes&&hash(raw)===record.sha256,`GIF bytes changed: ${record.relative_path}`);
  }
  assert(record.frames>1&&record.all_frames_decoded,`GIF not animation/decode verified: ${record.relative_path}`);
  assert(used.has(record.relative_path),`GIF not used by site: ${record.relative_path}`);
}
assert(used.size===92,'Expected all 92 GIFs referenced locally');
const scripts=[...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map(m=>m[1].split('?')[0]);
assert(scripts.indexOf('data/actions.js')<scripts.indexOf('assets/js/action-gallery.js'),'Action data must load before gallery');
assert(scripts.indexOf('assets/js/action-gallery.js')<scripts.indexOf('assets/js/app.js'),'Gallery must load before app');
for(const type of [...Object.keys(baseline.category_counts),'tools','action'])assert(html.includes(`data-type="${type}"`),`Missing category: ${type}`);
assert(!/<img[^>]+src="[^"]+\.gif/i.test(html),'Initial HTML must not eagerly load GIFs');
if(errors.length){console.error(errors.join('\n'));process.exit(1)}
console.log(JSON.stringify({result:'passed',original_records:baseline.data_count,original_categories:baseline.category_counts,
  action_boxes:M.ACTION_BOXES.length,actions:44,verified_gifs:used.size,original_files_preserved:Object.keys(baseline.original_files).length},null,2));
