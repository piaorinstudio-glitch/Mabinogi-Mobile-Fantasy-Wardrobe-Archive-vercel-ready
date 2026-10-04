// TW MapleStory display patch: Taiwan numbering only + pair next to same KR sequence.
(() => {
  const pairs = [
    {src:'image/tw-lucky-maple-1.png', label:'台版 #1', kr:'韓服 #1'},
    {src:'image/tw-pet-maple-2.png', label:'台版 #2', kr:'韓服 #2'}
  ];

  function apply(){
    const entries=[...document.querySelectorAll('#feed .entry')];
    for(const pair of pairs){
      const tw=entries.find(e=>{
        const img=e.querySelector('.image-wrap img');
        return img && (img.getAttribute('src')||'').endsWith(pair.src);
      });
      if(!tw) continue;

      const main=tw.querySelector('.num-badge-main');
      if(main) main.textContent=pair.label;

      const kr=[...document.querySelectorAll('#feed .entry')].find(e=>{
        if(e===tw) return false;
        const badge=e.querySelector('.num-badge-main');
        return badge && badge.textContent.trim()===pair.kr;
      });
      if(kr && kr.nextElementSibling!==tw) kr.after(tw);
    }
  }

  const observer=new MutationObserver(apply);
  observer.observe(document.getElementById('feed'),{childList:true,subtree:true});
  apply();
})();
