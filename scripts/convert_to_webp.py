from pathlib import Path
import argparse
from PIL import Image

parser=argparse.ArgumentParser(description='Convert a PNG/JPG image to web-ready WebP.')
parser.add_argument('source',type=Path)
parser.add_argument('target',type=Path,nargs='?')
parser.add_argument('--max-width',type=int,default=1600)
parser.add_argument('--quality',type=int,default=84)
args=parser.parse_args()
source=args.source
target=args.target or source.with_suffix('.webp')
if not source.exists(): raise SystemExit(f'File not found: {source}')
target.parent.mkdir(parents=True,exist_ok=True)
with Image.open(source) as im:
    im.load()
    if im.width>args.max_width:
        h=round(im.height*args.max_width/im.width)
        im=im.resize((args.max_width,h),Image.Resampling.LANCZOS)
    if im.mode not in {'RGB','RGBA'}:
        im=im.convert('RGBA' if 'transparency' in im.info else 'RGB')
    im.save(target,'WEBP',quality=args.quality,method=6)
print(target)
