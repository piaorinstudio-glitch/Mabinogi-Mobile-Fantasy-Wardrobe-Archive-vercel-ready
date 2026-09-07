global.window=global;
require('../data/catalog.js');
require('../data/pets.js');
require('../data/site-config.js');
const {DATA,PET_STATS,PET_FAMILY_BY_KO,PET_SKILL_FAMILIES,TW_CURRENT_IDS,TW_RELEASED_IDS,TOOL_LINKS}=MABI;
const errors=[];
const ids=new Set();
const allowedTypes=new Set(['pass','lucky','package','legend','pet','abyss','raid']);
for(const item of DATA){
  if(ids.has(item.id)) errors.push(`duplicate id: ${item.id}`); ids.add(item.id);
  if(!allowedTypes.has(item.type)) errors.push(`unknown type: ${item.id} -> ${item.type}`);
  if(!/^\d{4}-\d{2}-\d{2}$/.test(item.date||'')) errors.push(`bad date: ${item.id} -> ${item.date}`);
  if(String(item.year)!==String(item.date||'').slice(0,4)) errors.push(`year/date mismatch: ${item.id}`);
  if(!item.zh&&!item.ko) errors.push(`missing display name: ${item.id}`);
  for(const key of ['image','regularImage','hoodedImage','sourceImage']){
    const value=item[key]; if(!value) continue;
    if(!/^https:\/\//.test(value) && !/^(image|assets)\//.test(value)) errors.push(`unexpected ${key} path: ${item.id} -> ${value}`);
  }
}
for(const setName of ['TW_CURRENT_IDS','TW_RELEASED_IDS']){
  const set=MABI[setName];
  for(const id of set) if(!ids.has(id)) errors.push(`${setName} contains unknown id: ${id}`);
}
for(const item of DATA.filter(x=>x.type==='pet')){
  for(const v of item.variants||[]){
    if(typeof v!=='object') continue;
    if(!PET_STATS[v.ko]) errors.push(`pet stats missing: ${v.ko} (${item.id})`);
    const fam=PET_FAMILY_BY_KO[v.ko];
    if(!fam) errors.push(`pet family missing: ${v.ko} (${item.id})`);
    else if(!PET_SKILL_FAMILIES[fam]) errors.push(`pet skill family missing: ${fam} (${v.ko})`);
  }
}
const count=(t)=>DATA.filter(x=>x.type===t).length;
if(errors.length){console.error(errors.map(x=>'ERROR: '+x).join('\n'));process.exit(1);}
console.log(`OK: ${DATA.length} archive entries; ${DATA.filter(x=>x.type==='pet').reduce((n,x)=>n+(x.variants||[]).length,0)} pet variants; ${Object.keys(PET_SKILL_FAMILIES).length} pet skill families; ${TOOL_LINKS.length} shared tool(s).`);
