from pathlib import Path
import re, sys, subprocess
ROOT=Path(__file__).resolve().parents[1]
ERRORS=[]
PROD_TEXT=['index.html','about.html','privacy.html','contact.html','sitemap.xml','robots.txt']
for rel in PROD_TEXT:
    if not (ROOT/rel).exists(): ERRORS.append(f'missing required file: {rel}')
# Local src/href references in HTML.
for html in ROOT.glob('*.html'):
    text=html.read_text(encoding='utf-8')
    for attr,url in re.findall(r'\b(src|href)="([^"]+)"',text):
        if re.match(r'^(https?:|mailto:|#)',url): continue
        target=(html.parent/url.split('#')[0].split('?')[0]).resolve()
        if not target.exists(): ERRORS.append(f'{html.name}: missing {url}')
# Data image paths.
for js in [ROOT/'data/catalog.js']:
    text=js.read_text(encoding='utf-8')
    for url in re.findall(r'"(?:image|regularImage|hoodedImage|sourceImage)"\s*:\s*"([^"]+)"',text):
        if re.match(r'^https?://',url): continue
        if not (ROOT/url).exists(): ERRORS.append(f'{js.relative_to(ROOT)}: missing {url}')
# JS syntax, individually and in browser load order (catches duplicate global const/let declarations).
js_files=list((ROOT/'assets/js').glob('*.js'))+list((ROOT/'data').glob('*.js'))
for js in js_files:
    cp=subprocess.run(['node','--check',str(js)],capture_output=True,text=True)
    if cp.returncode: ERRORS.append(f'{js.relative_to(ROOT)}: JS syntax error\n{cp.stderr}')
load_order=[ROOT/'data/ads-config.js',ROOT/'assets/js/ads.js',ROOT/'data/catalog.js',ROOT/'data/pets.js',ROOT/'data/site-config.js',ROOT/'assets/js/app.js']
combined='\n'.join(f.read_text(encoding='utf-8') for f in load_order)
tmp=ROOT/'.validate-combined.js'; tmp.write_text(combined,encoding='utf-8')
cp=subprocess.run(['node','--check',str(tmp)],capture_output=True,text=True)
tmp.unlink(missing_ok=True)
if cp.returncode: ERRORS.append(f'combined browser script order: JS syntax/global declaration error\n{cp.stderr}')
data_check=subprocess.run(['node',str(ROOT/'scripts/validate_data.js')],capture_output=True,text=True,cwd=ROOT/'scripts')
if data_check.returncode: ERRORS.append('data consistency check failed\n'+data_check.stderr)
if ERRORS:
    print('\n'.join('ERROR: '+e for e in ERRORS)); sys.exit(1)
print('OK: required pages, local references, image references, and JavaScript syntax passed.')
