from pathlib import Path
import re

INDEX = Path('index.html')
if not INDEX.exists():
    raise SystemExit('index.html not found. Please run this from the repository root.')

text = INDEX.read_text(encoding='utf-8')

footer_css_marker = '/* credit footer */'
footer_css = r'''

/* credit footer */
.site-footer{
  padding:10px 0 42px;
  color:var(--muted);
  text-align:center;
  font-size:11px;
  line-height:1.75;
}
.site-footer .credit-main{
  color:#3f4d43;
  font-weight:900;
  letter-spacing:.02em;
}
.site-footer .credit-note{
  margin-top:4px;
  opacity:.86;
}
@media(max-width:620px){
  .site-footer{
    padding:8px 10px 34px;
    font-size:10px;
    line-height:1.65;
  }
}
'''
if footer_css_marker not in text:
    text = text.replace('\n</style>', footer_css + '\n</style>', 1)

new_footer = '''<footer class="wrap site-footer">
  <div class="credit-main">Mabinogi Mobile KR 外觀整理｜整理與網頁製作：飄鈴</div>
  <div class="credit-note">本網站為玩家整理資料，非官方網站。遊戲名稱、圖片與相關素材版權屬原權利方所有。</div>
</footer>'''

text, count = re.subn(r'<footer\s+class="wrap(?:\s+site-footer)?">.*?</footer>', new_footer, text, count=1, flags=re.S)
if count == 0:
    text = text.replace('</main>', '</main>\n' + new_footer, 1)

text = re.sub(r'<!-- credit footer [^>]*-->\n?', '', text)
text = text.replace('</html>', '<!-- credit footer 2026-09-05 -->\n</html>')

INDEX.write_text(text, encoding='utf-8', newline='\n')
print('Credit footer applied: 飄鈴')
