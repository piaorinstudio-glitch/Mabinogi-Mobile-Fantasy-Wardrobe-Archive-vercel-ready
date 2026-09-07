from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

# 1) Put sorting / prediction controls into a separate toolbar action row.
if 'id="toolbarActions"' not in text:
    pattern = re.compile(
        r'(\s*</nav>\s*)'
        r'(<button class="predict-btn"[\s\S]*?'
        r'<select class="sort" id="sort"[\s\S]*?</select>)',
        re.M
    )
    text, count = pattern.subn(
        r'\1<div class="toolbar-actions" id="toolbarActions">\n    \2\n    </div>',
        text,
        count=1
    )
    if count == 0:
        raise SystemExit('Could not find toolbar controls to wrap. Please check index.html structure.')

# 2) Append CSS overrides. Last block wins over previous mobile rules.
marker = '/* mobile toolbar separation fix */'
css = r'''

/* mobile toolbar separation fix */
.toolbar-actions{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:8px;
  flex:0 0 auto;
  margin-left:auto;
}
.toolbar-actions .sort{margin-left:0;}

@media(max-width:900px){
  .toolbar{
    display:flex;
    flex-wrap:wrap;
    align-items:stretch;
    row-gap:0;
    padding:10px 0 11px;
  }
  .toolbar .category-nav{
    order:1;
    flex:1 0 100%;
    width:100%;
    max-width:100%;
    display:flex;
    flex-wrap:nowrap;
    overflow-x:auto;
    gap:7px;
    padding:0 2px 8px;
    margin:0 -2px;
    border-bottom:1px solid rgba(199,184,150,.46);
    scrollbar-width:thin;
  }
  .toolbar .category{
    flex:0 0 auto;
    white-space:nowrap;
  }
  .toolbar-actions{
    order:2;
    flex:1 0 100%;
    width:100%;
    margin-left:0;
    padding-top:8px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
  }
  .toolbar-actions .predict-btn.show{
    display:inline-flex;
    order:1;
    flex:0 1 auto;
    justify-content:center;
  }
  .toolbar-actions .offline-pet-btn.show{
    display:inline-flex;
    order:1;
  }
  .toolbar-actions .sort{
    order:2;
    flex:0 0 auto;
    margin-left:auto;
    min-width:112px;
  }
}

@media(max-width:620px){
  .toolbar-actions{
    padding:8px;
    border:1px solid rgba(199,184,150,.38);
    border-radius:13px;
    background:rgba(255,253,248,.48);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.5);
  }
  .toolbar-actions .predict-btn.show{
    flex:1 1 156px;
    min-width:0;
    height:37px;
    padding:0 10px;
  }
  .toolbar-actions .sort{
    height:37px;
    min-width:104px;
    max-width:116px;
  }
}

@media(max-width:390px){
  .toolbar-actions{
    gap:6px;
    padding:7px;
  }
  .toolbar-actions .predict-btn.show{
    font-size:11px;
    padding:0 8px;
  }
  .toolbar-actions .sort{
    min-width:98px;
    max-width:108px;
    font-size:11px;
  }
}
'''
if marker not in text:
    text = text.replace('\n</style>', css + '\n</style>', 1)

# 3) Make sure render can continue to find the same button/select IDs.
# No JS changes required because IDs remain unchanged.

# 4) Bump marker for GitHub Pages redeploy.
text = re.sub(r'\n<!-- mobile toolbar fix [^>]*-->', '', text)
text = text.replace('</html>', '\n<!-- mobile toolbar fix 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Mobile toolbar layout fixed: category row separated from prediction and sorting controls.')
