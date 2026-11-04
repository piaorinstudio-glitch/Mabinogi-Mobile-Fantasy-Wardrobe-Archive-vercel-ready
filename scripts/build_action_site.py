#!/usr/bin/env python3
"""GitHub Pages build: restore action-box gallery using on-demand MP4 videos.

All GIF inputs are read from the existing repository and never published.
Public artifact only includes cover PNG and converted H.264 MP4 files.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "site-dist"
CACHE = ROOT / "action-video-cache"
NAV = '<button class="category" data-type="tools"><span class="cat-zh">小工具</span><span class="cat-en">TOOLS</span></button>'
ACTION_NAV = '<button class="category" data-type="action"><span class="cat-zh">動作箱</span><span class="cat-en">ACTION</span></button>'
APP_SCRIPT = '<script defer src="assets/js/app.js?v=20261016-pet-fix"></script>'
SCRIPTS = ('<script defer src="data/actions.js?v=20261104-mp4"></script>'
           '<script defer src="assets/js/action-gallery-video.js?v=20261104-mp4"></script>')
OLD_IMG = '<div class="action-gif-frame"><img id="actionGif" alt="" decoding="async"></div>'
NEW_VIDEO = ('<div class="action-gif-frame"><video id="actionVideo" controls muted loop '
             'playsinline preload="none" aria-label="動作影片預覽"></video></div>')
# Only "path" keys are rewritten. The original GIF sourceUrl records remain intact for citations.
GIF_PREVIEW_PATH = re.compile(r'("path"\s*:\s*"image/actions/[^"\r\n]+)\.gif(")', re.IGNORECASE)
PNG_REFERENCES = re.compile(r'"(?:cover|image)"\s*:\s*"(image/actions/[^"\r\n]+\.png)"', re.IGNORECASE)
VIDEO_REFERENCES = re.compile(r'"path"\s*:\s*"(image/actions/[^"\r\n]+\.mp4)"', re.IGNORECASE)


def run(cmd: list[str], *, quiet: bool = False) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL if quiet else None)


def require_once(content: str, old: str, what: str) -> None:
    if content.count(old) != 1:
        raise RuntimeError(f"{what}: expected one match, got {content.count(old)}. Refusing unsafe edit.")


def build(*, no_encode: bool = False) -> None:
    if not (ROOT / 'index.html').is_file() or not (ROOT / 'data/actions.js').is_file():
        raise RuntimeError('Missing index.html or data/actions.js in the GitHub repository root')
    if shutil.which('rsync') is None:
        raise RuntimeError('rsync is required on the GitHub runner')
    if not no_encode and shutil.which('ffmpeg') is None:
        raise RuntimeError('ffmpeg is required on the GitHub runner')
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    # Exclude heavyweight GIF originals from the public website (but preserve other categories).
    run(['rsync', '-a', '--exclude=/.git/', '--exclude=/.github/', '--exclude=/site-dist/',
         '--exclude=/action-video-cache/', '--exclude=/image/actions/',
         '--exclude=/assets/js/action-gallery.js', '--exclude=/research/',
         '--exclude=/docs/', '--exclude=/scripts/', '--exclude=/*.py',
         '--exclude=/*.json', '--exclude=/*.txt', './', 'site-dist/'], quiet=True)

    html_path = DIST / 'index.html'
    html = html_path.read_text(encoding='utf-8')
    # The action category was disabled on 2026-11-02; restore it before Tools.
    if ACTION_NAV not in html:
        require_once(html, NAV, 'Tools nav button')
        html = html.replace(NAV, ACTION_NAV + NAV, 1)
    if 'data/actions.js?' not in html:
        require_once(html, APP_SCRIPT, 'app.js script')
        html = html.replace(APP_SCRIPT, SCRIPTS + APP_SCRIPT, 1)
    # Change the former image-only GIF viewer into a native video player.
    if OLD_IMG in html:
        require_once(html, OLD_IMG, 'old GIF viewer')
        html = html.replace(OLD_IMG, NEW_VIDEO, 1)
    elif NEW_VIDEO not in html:
        raise RuntimeError('Action preview HTML does not match expected layout')
    assert html.count('data-type="action"') == 1
    assert 'assets/js/action-gallery-video.js?' in html
    html_path.write_text(html, encoding='utf-8')

    # Preserve original library records in GitHub, rewrite only *published* preview paths.
    actions_source = (ROOT / 'data/actions.js').read_text(encoding='utf-8')
    actions_published, replacements = GIF_PREVIEW_PATH.subn(r'\1.mp4\2', actions_source)
    if not replacements:
        raise RuntimeError('No GIF previews found in existing data/actions.js; check format')
    action_data_out = DIST / 'data/actions.js'
    action_data_out.parent.mkdir(parents=True, exist_ok=True)
    action_data_out.write_text(actions_published, encoding='utf-8')
    video_paths = set(VIDEO_REFERENCES.findall(actions_published))
    png_paths = set(PNG_REFERENCES.findall(actions_published))
    if replacements < len(video_paths):
        raise RuntimeError(f'MP4 preview count {len(video_paths)} exceeds preview references {replacements}')

    for path in sorted(png_paths):
        src = ROOT / path
        if not src.is_file():
            raise RuntimeError(f'Missing cover: {path}')
        dst = DIST / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    for idx, path in enumerate(sorted(video_paths), 1):
        gif = ROOT / path.replace('.mp4', '.gif')
        cache_mp4 = CACHE / path
        dst_mp4 = DIST / path
        if not gif.is_file():
            raise RuntimeError(f'Original source GIF absent: {gif}')
        if not cache_mp4.is_file() or cache_mp4.stat().st_size < 100:
            if no_encode:
                raise RuntimeError(f'Cached MP4 missing: {cache_mp4}')
            cache_mp4.parent.mkdir(parents=True, exist_ok=True)
            temp_mp4 = cache_mp4.with_suffix('.tmp.mp4')
            print(f'[{idx}/{len(video_paths)}] {gif.relative_to(ROOT)} => MP4', flush=True)
            try:
                run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(gif),
                     '-vf', 'fps=12,scale=480:480:force_original_aspect_ratio=decrease:force_divisible_by=2',
                     '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '32',
                     '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', str(temp_mp4)], quiet=True)
                if not temp_mp4.is_file() or temp_mp4.stat().st_size < 100:
                    raise RuntimeError(f'ffmpeg output missing for {path}')
                if temp_mp4.stat().st_size >= gif.stat().st_size:
                    raise RuntimeError(f'Encoded video is not smaller than GIF: {path}')
                temp_mp4.replace(cache_mp4)
            finally:
                temp_mp4.unlink(missing_ok=True)
        dst_mp4.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cache_mp4, dst_mp4)

    css = DIST / 'assets/css/main.css'
    with css.open('a', encoding='utf-8') as f:
        f.write('\n/* Video-only action previews: avoid GIF downloads. */\n'
                '.action-gif-frame video{display:block;width:auto;max-width:100%;height:auto;max-height:52vh;object-fit:contain;background:#f2ecdf}\n'
                '@media(max-width:700px){.action-gif-frame video{max-height:46vh}}\n')

    # Fail deployment rather than publish cards with absent or mismatched videos.
    missing = [path for path in video_paths | png_paths if not (DIST / path).is_file()]
    leaked_gifs = list((DIST / 'image/actions').rglob('*.gif'))
    if missing or leaked_gifs:
        raise RuntimeError(f'Validation failed: missing={missing[:5]}, published GIFs={leaked_gifs[:5]}')
    if GIF_PREVIEW_PATH.search(action_data_out.read_text(encoding='utf-8')):
        raise RuntimeError('Unconverted GIF preview path remains in published data/actions.js')
    if not (DIST / 'assets/js/action-gallery-video.js').is_file():
        raise RuntimeError('Video gallery JS missing in deployed files')
    (DIST / '.nojekyll').touch()
    mp4_bytes = sum((DIST / p).stat().st_size for p in video_paths)
    full_bytes = sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())
    print(f'Validated {len(video_paths)} MP4 videos, {len(png_paths)} PNG covers, 0 published GIFs.')
    print(f'MP4 total: {mp4_bytes / 1048576:.1f} MiB; website total: {full_bytes / 1048576:.1f} MiB.')
    print('HTML action tab and video data scripts: OK')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-encode', action='store_true', help='Use only existing cached MP4s')
    args = parser.parse_args()
    try:
        build(no_encode=args.no_encode)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'BUILD FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
