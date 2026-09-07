from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

# Remove previous copies of this patch if re-run.
text = re.sub(r'\n?/\* requested scrapbook ui fix v1 \*/[\s\S]*?(?=\n</style>)', '', text, count=1)
text = re.sub(r'\n?<script id="mabi-requested-ui-fix">[\s\S]*?</script>\s*', '\n', text, count=1)

# Clean up a few common bad placeholder states directly in HTML.
text = text.replace('value="undefined"', 'value=""')
text = text.replace('placeholder="undefined"', 'placeholder="搜尋中文名 / 韓文名"')
text = text.replace('placeholder="中文名 / 韓文名 / 來源 / 期數"', 'placeholder="搜尋中文名 / 韓文名"')
text = text.replace('placeholder="中文名 / 韓文名"', 'placeholder="搜尋中文名 / 韓文名"')
text = text.replace('placeholder="搜尋中文名 / 韓文名 / 來源 / 期數"', 'placeholder="搜尋中文名 / 韓文名"')

style = r'''

/* requested scrapbook ui fix v1 */
html.mabi-scrapbook-final .hero::before,
html.mabi-scrapbook-final .hero::after,
html.mabi-scrapbook-final .hero-top::before,
html.mabi-scrapbook-final .hero-top::after{content:none !important;display:none !important;}
html.mabi-scrapbook-final .eyebrow,
html.mabi-scrapbook-final .subtitle,
html.mabi-scrapbook-final .section-note,
html.mabi-scrapbook-final .hero-note,
html.mabi-scrapbook-final .hero-note-card,
html.mabi-scrapbook-final .hero-sticker,
html.mabi-scrapbook-final .hero-polaroid .hero-note-text{display:none !important;}

html.mabi-scrapbook-final .hero{padding:24px 0 18px !important;}
html.mabi-scrapbook-final .hero-top{
  min-height:0 !important;
  padding:8px 140px 6px !important;
  display:block !important;
  text-align:center !important;
}
html.mabi-scrapbook-final .hero-top > div{max-width:760px;margin:0 auto;}
html.mabi-scrapbook-final .hero h1{
  margin:0 auto !important;
  display:flex !important;
  flex-direction:column !important;
  align-items:center !important;
  justify-content:center !important;
  gap:6px !important;
  color:#332e2b !important;
  line-height:1.04 !important;
  letter-spacing:-.03em !important;
  text-shadow:none !important;
}
html.mabi-scrapbook-final .hero h1 .mabi-title-small{
  display:block;
  font-size:clamp(28px,3.3vw,40px);
  font-weight:800;
  letter-spacing:.04em;
}
html.mabi-scrapbook-final .hero h1 .mabi-title-main{
  display:block;
  font-size:clamp(46px,6.1vw,84px);
  font-weight:950;
}
html.mabi-scrapbook-final .source-btn{
  top:8px !important;
  right:0 !important;
}

html.mabi-scrapbook-final .toolbar-shell{margin-top:0 !important;}
html.mabi-scrapbook-final .category::before,
html.mabi-scrapbook-final .category::after{content:none !important;display:none !important;}
html.mabi-scrapbook-final .category{
  min-width:138px !important;
  height:56px !important;
  padding:0 18px !important;
  gap:2px !important;
}
html.mabi-scrapbook-final .category .cat-zh{font-size:13px !important;line-height:1.1 !important;letter-spacing:.08em !important;}
html.mabi-scrapbook-final .category .cat-en{font-size:10px !important;letter-spacing:.16em !important;opacity:.75;}

html.mabi-scrapbook-final main.wrap{padding-top:24px !important;}
html.mabi-scrapbook-final .section-head{
  display:flex !important;
  align-items:center !important;
  justify-content:space-between !important;
  gap:18px !important;
  margin:0 0 14px !important;
}
html.mabi-scrapbook-final .mabi-head-top{
  display:flex !important;
  align-items:center !important;
  gap:18px !important;
  min-width:0 !important;
}
html.mabi-scrapbook-final .mabi-head-actions{
  display:flex !important;
  align-items:center !important;
  justify-content:flex-end !important;
  gap:12px !important;
  flex-wrap:wrap !important;
}
html.mabi-scrapbook-final .mabi-head-sub{
  display:grid !important;
  grid-template-columns:minmax(0,1fr) auto !important;
  align-items:center !important;
  gap:16px !important;
  margin:0 0 18px !important;
}
html.mabi-scrapbook-final .section-title{
  min-width:220px !important;
  min-height:64px !important;
  padding:14px 28px !important;
  font-size:clamp(28px,3.8vw,50px) !important;
  line-height:1 !important;
}
html.mabi-scrapbook-final .section-title::after{font-size:.40em !important;letter-spacing:.24em !important;}
html.mabi-scrapbook-final .archive-tools,
html.mabi-scrapbook-final .mabi-search-shell{
  display:flex !important;
  align-items:center !important;
  gap:12px !important;
  min-width:0 !important;
  width:100% !important;
}
html.mabi-scrapbook-final .archive-search-wrap{
  display:flex !important;
  align-items:center !important;
  gap:12px !important;
  width:min(680px,100%) !important;
  max-width:100% !important;
  height:58px !important;
  padding:0 18px !important;
  border-radius:999px !important;
  border:2px solid #bfd7c5 !important;
  background:rgba(255,255,255,.90) !important;
  box-shadow:0 10px 24px rgba(113,96,74,.08), inset 0 1px 0 rgba(255,255,255,.86) !important;
}
html.mabi-scrapbook-final .archive-search-wrap > span{
  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;
  width:44px !important;
  min-width:44px !important;
  height:44px !important;
  border-radius:999px !important;
  background:#dce9df !important;
  color:#6b675d !important;
  font-size:0 !important;
  position:relative !important;
}
html.mabi-scrapbook-final .archive-search-wrap > span::before{
  content:'⌕';
  font-size:26px;
  line-height:1;
}
html.mabi-scrapbook-final .archive-search{
  width:100% !important;
  min-width:0 !important;
  border:0 !important;
  outline:0 !important;
  background:transparent !important;
  color:#514943 !important;
  font-size:14px !important;
  font-weight:900 !important;
}
html.mabi-scrapbook-final .archive-search::placeholder{color:#8f877f !important;opacity:1;}
html.mabi-scrapbook-final .archive-count,
html.mabi-scrapbook-final .mabi-count-inline{
  white-space:nowrap !important;
  color:#6c625b !important;
  font-size:15px !important;
  font-weight:900 !important;
}
html.mabi-scrapbook-final .mabi-head-actions .sort,
html.mabi-scrapbook-final .mabi-head-actions .predict-btn,
html.mabi-scrapbook-final .mabi-head-actions .offline-pet-btn{
  height:52px !important;
  padding:0 22px !important;
  border-radius:999px !important;
}

html.mabi-scrapbook-final .mabi-pet-kind-filters{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  margin:-2px 0 18px;
}
html.mabi-scrapbook-final .mabi-pet-kind-filters button{
  height:40px;
  padding:0 16px;
  border-radius:999px;
  border:1px solid rgba(220,204,178,.9);
  background:rgba(255,255,255,.86);
  color:#655b53;
  font-size:13px;
  font-weight:900;
  box-shadow:0 6px 14px rgba(107,93,74,.07);
  cursor:pointer;
}
html.mabi-scrapbook-final .mabi-pet-kind-filters button.active{color:#fff;border-color:transparent;}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="all"].active{background:linear-gradient(180deg,#95c9a8,#6aa98b);}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="常駐"],
html.mabi-scrapbook-final .mabi-kind-chip.regular{background:linear-gradient(180deg,#95c9a8,#6aa98b);}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="限定"],
html.mabi-scrapbook-final .mabi-kind-chip.limited{background:linear-gradient(180deg,#e3c07b,#c99943);}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="聯動"],
html.mabi-scrapbook-final .mabi-kind-chip.collab{background:linear-gradient(180deg,#b7a2db,#8f74c1);}
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="常駐"].active,
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="限定"].active,
html.mabi-scrapbook-final .mabi-pet-kind-filters button[data-kind="聯動"].active{color:#fff;border-color:transparent;}

html.mabi-scrapbook-final .feed{
  display:grid !important;
  grid-template-columns:repeat(4,minmax(0,1fr)) !important;
  gap:22px !important;
}
html.mabi-scrapbook-final .entry{
  overflow:visible !important;
  border-radius:16px !important;
  background:#fffdfa !important;
  box-shadow:0 10px 28px rgba(103,88,69,.10) !important;
}
html.mabi-scrapbook-final .image-wrap{
  aspect-ratio:1 / 0.88 !important;
  border-radius:14px 14px 0 0 !important;
  overflow:visible !important;
}
html.mabi-scrapbook-final .image-wrap::after{display:none !important;}
html.mabi-scrapbook-final .image-wrap img{
  width:calc(100% - 16px) !important;
  height:calc(100% - 16px) !important;
  margin:8px !important;
  border-radius:4px !important;
  object-fit:cover !important;
  box-shadow:none !important;
}
html.mabi-scrapbook-final .entry-info{
  padding:16px 18px 14px !important;
  display:flex !important;
  flex-direction:column !important;
  justify-content:flex-start !important;
  gap:3px !important;
}
html.mabi-scrapbook-final .entry-meta,
html.mabi-scrapbook-final .date{display:none !important;}
html.mabi-scrapbook-final .name{
  font-size:19px !important;
  line-height:1.25 !important;
  letter-spacing:-.02em !important;
}
html.mabi-scrapbook-final .ko{
  margin-top:2px !important;
  font-size:13px !important;
  line-height:1.35 !important;
}
html.mabi-scrapbook-final .mabi-num-badge{
  position:absolute;
  right:16px;
  bottom:-14px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  min-width:74px;
  height:74px;
  padding:10px 12px;
  border-radius:8px;
  background:#efe5d3;
  color:#655a4f;
  font-size:14px;
  font-weight:900;
  box-shadow:0 10px 20px rgba(104,86,63,.12);
  z-index:3;
}
html.mabi-scrapbook-final .mabi-kind-chip{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  align-self:flex-start;
  height:28px;
  padding:0 10px;
  border-radius:999px;
  color:#fff;
  font-size:12px;
  font-weight:900;
  margin-bottom:6px;
}
html.mabi-scrapbook-final .pet-variants{margin-top:8px !important;}
html.mabi-scrapbook-final .pet-variant{padding:6px 8px !important;}

@media (max-width:1080px){
  html.mabi-scrapbook-final .hero-top{padding:8px 80px 6px !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(3,minmax(0,1fr)) !important;}
}
@media (max-width:820px){
  html.mabi-scrapbook-final .hero-top{padding:8px 16px 6px !important;}
  html.mabi-scrapbook-final .source-btn{position:static !important;margin:14px auto 0 !important;display:inline-flex !important;}
  html.mabi-scrapbook-final .section-head,
  html.mabi-scrapbook-final .mabi-head-sub{display:flex !important;flex-direction:column !important;align-items:stretch !important;}
  html.mabi-scrapbook-final .mabi-head-actions{justify-content:flex-start !important;}
  html.mabi-scrapbook-final .archive-search-wrap{width:100% !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:repeat(2,minmax(0,1fr)) !important;}
}
@media (max-width:560px){
  html.mabi-scrapbook-final .category{min-width:110px !important;height:52px !important;}
  html.mabi-scrapbook-final .feed{grid-template-columns:1fr !important;gap:18px !important;}
  html.mabi-scrapbook-final .mabi-num-badge{min-width:68px;height:68px;font-size:13px;}
}
'''

script = r'''
<script id="mabi-requested-ui-fix">
(()=>{
  const TYPE_LABELS = {
    pass:['通行證','PASS'],
    lucky:['幸運箱','LUCKY BOX'],
    package:['全套套組','SET ITEM'],
    dye:['染色預覽','DYE PREVIEW'],
    pet:['寵物','PET'],
    abyss:['深淵副本時裝','ABYSS'],
    raid:['團隊副本時裝','RAID']
  };
  let petKindFilter = 'all';

  const q = (sel, root=document) => root.querySelector(sel);
  const qa = (sel, root=document) => Array.from(root.querySelectorAll(sel));

  function itemFromEntry(entry){
    const id = q('.image-wrap', entry)?.dataset?.image;
    return (typeof DATA !== 'undefined' && DATA.find) ? DATA.find(x => x.id === id) : null;
  }
  function kindClass(kind){
    if(kind === '限定') return 'limited';
    if(kind === '聯動') return 'collab';
    return 'regular';
  }
  function issueText(item){
    if(!item) return '';
    if(item.type === 'package') return `第 ${item.number} 代`;
    if(item.type === 'abyss' || item.type === 'raid') return `第 ${item.number} 套`;
    return `第 ${item.number} 期`;
  }

  function tuneHeader(){
    const h1 = q('.hero h1');
    if(h1 && !h1.querySelector('.mabi-title-small')){
      h1.innerHTML = '<span class="mabi-title-small">瑪奇Mobile</span><span class="mabi-title-main">韓服外觀圖鑑</span>';
    }
    const eyebrow = q('.hero .eyebrow'); if(eyebrow) eyebrow.textContent = '';
    const subtitle = q('.hero .subtitle'); if(subtitle) subtitle.textContent = '';
    const note = q('#sectionNote'); if(note) note.textContent = '';
  }

  function tuneCategories(){
    qa('.category').forEach(btn => {
      const [zh,en] = TYPE_LABELS[btn.dataset.type] || [btn.textContent.trim(), ''];
      if(!btn.querySelector('.cat-zh')){
        btn.innerHTML = `<span class="cat-zh">${zh}</span>${en ? `<span class="cat-en">${en}</span>` : ''}`;
      }
    });
  }

  function ensureSearchTools(){
    const main = q('main.wrap');
    if(!main) return;
    const head = q('.section-head', main);
    if(!head) return;

    let top = q('.mabi-head-top', head);
    let actions = q('.mabi-head-actions', head);
    const title = q('#sectionTitle', head) || q('#sectionTitle');
    const note = q('#sectionNote', head) || q('#sectionNote');
    const sort = q('#sort');
    const predict = q('#openPrediction');
    const offlinePetBtn = q('#offlinePetBtn');

    if(!top || !actions){
      head.innerHTML = '';
      top = document.createElement('div');
      top.className = 'mabi-head-top';
      if(title) top.appendChild(title);
      if(note) top.appendChild(note);
      actions = document.createElement('div');
      actions.className = 'mabi-head-actions';
      head.appendChild(top);
      head.appendChild(actions);
    }
    if(sort && sort.parentElement !== actions) actions.appendChild(sort);
    if(predict && predict.parentElement !== actions) actions.appendChild(predict);
    if(offlinePetBtn && offlinePetBtn.parentElement !== actions) actions.appendChild(offlinePetBtn);

    let sub = q('.mabi-head-sub', main);
    if(!sub){
      sub = document.createElement('div');
      sub.className = 'mabi-head-sub';
      head.insertAdjacentElement('afterend', sub);
    }
    const searchWrap = q('#archiveTools') || q('.archive-tools');
    const count = q('#archiveCount') || q('.archive-count');
    if(searchWrap){
      searchWrap.classList.add('mabi-search-shell');
      if(searchWrap.parentElement !== sub) sub.appendChild(searchWrap);
      const input = q('#archiveSearch', searchWrap);
      if(input){
        input.placeholder = '搜尋中文名 / 韓文名';
        if(input.value === 'undefined') input.value = '';
      }
      const searchLabel = q('.archive-search-wrap > span', searchWrap);
      if(searchLabel) searchLabel.textContent = '';
    }
    if(count && count.parentElement !== sub) sub.appendChild(count);
  }

  function tuneEntry(entry){
    const item = itemFromEntry(entry);
    if(!item) return;
    const wrap = q('.image-wrap', entry);
    const info = q('.entry-info', entry);
    const meta = q('.entry-meta', entry);
    if(meta) meta.style.display = 'none';
    if(wrap){
      let badge = q('.mabi-num-badge', wrap);
      if(!badge){
        badge = document.createElement('span');
        badge.className = 'mabi-num-badge';
        wrap.appendChild(badge);
      }
      badge.textContent = issueText(item);
    }
    if(info){
      let chip = q('.mabi-kind-chip', info);
      if(item.type === 'pet'){
        if(!chip){
          chip = document.createElement('div');
          chip.className = 'mabi-kind-chip';
          info.insertBefore(chip, info.firstChild);
        }
        chip.className = `mabi-kind-chip ${kindClass(item.kind)}`;
        chip.textContent = item.kind || '常駐';
      }else if(chip){
        chip.remove();
      }
    }
  }

  function visibleFeedCount(){
    return qa('#feed .entry').filter(el => getComputedStyle(el).display !== 'none').length;
  }

  function updateCount(){
    const count = q('#archiveCount') || q('.archive-count');
    if(count) count.textContent = `共 ${visibleFeedCount()} 筆`;
  }

  function ensurePetFilters(){
    const main = q('main.wrap');
    if(!main) return;
    let bar = q('#mabiPetKindFilters', main);
    const shouldShow = typeof state !== 'undefined' && state.type === 'pet';
    if(!shouldShow){
      if(bar) bar.remove();
      return;
    }
    if(!bar){
      bar = document.createElement('div');
      bar.id = 'mabiPetKindFilters';
      bar.className = 'mabi-pet-kind-filters';
      const base = q('.mabi-head-sub', main) || q('.section-head', main);
      if(base) base.insertAdjacentElement('afterend', bar);
      ['all','常駐','限定','聯動'].forEach(kind => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.dataset.kind = kind;
        btn.textContent = kind === 'all' ? '全部' : kind;
        btn.addEventListener('click', () => {
          petKindFilter = kind;
          applyPetFilters();
          qa('button', bar).forEach(x => x.classList.toggle('active', x.dataset.kind === petKindFilter));
        });
        bar.appendChild(btn);
      });
    }
    qa('button', bar).forEach(x => x.classList.toggle('active', x.dataset.kind === petKindFilter));
    applyPetFilters();
  }

  function applyPetFilters(){
    if(!(typeof state !== 'undefined' && state.type === 'pet')) return;
    qa('#feed .entry').forEach(entry => {
      const item = itemFromEntry(entry);
      const show = !item || petKindFilter === 'all' || item.kind === petKindFilter;
      entry.style.display = show ? '' : 'none';
    });
    updateCount();
  }

  function refresh(){
    tuneHeader();
    tuneCategories();
    ensureSearchTools();
    qa('#feed .entry').forEach(tuneEntry);
    ensurePetFilters();
    updateCount();
  }

  const feed = q('#feed');
  if(feed){
    new MutationObserver(() => setTimeout(refresh, 0)).observe(feed, {childList:true, subtree:true});
  }

  document.addEventListener('DOMContentLoaded', () => setTimeout(refresh, 80));
  window.addEventListener('hashchange', () => setTimeout(refresh, 80));
  document.addEventListener('click', e => {
    if(e.target.closest('.category')) setTimeout(refresh, 80);
  });
  document.addEventListener('change', e => {
    if(e.target.id === 'sort') setTimeout(refresh, 80);
  });
  document.addEventListener('input', e => {
    if(e.target.id === 'archiveSearch') setTimeout(updateCount, 30);
  });
  setTimeout(refresh, 140);
})();
</script>
'''

if '</style>' not in text:
    raise SystemExit('Could not find </style> in index.html')
text = text.replace('\n</style>', style + '\n</style>', 1)

if '</body>' not in text:
    raise SystemExit('Could not find </body> in index.html')
text = text.replace('</body>', script + '\n</body>', 1)

INDEX.write_text(text, encoding='utf-8')
print('Applied requested scrapbook UI fix patch to index.html')
