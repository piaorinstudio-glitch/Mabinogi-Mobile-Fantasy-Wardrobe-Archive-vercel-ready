"""Create web-ready WebP copies and update index.html to use them."""

from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = PROJECT_ROOT / "index.html"
IMAGE_ROOTS = (PROJECT_ROOT / "image", PROJECT_ROOT / "assets")
MAX_WIDTH = 1600
QUALITY = 82


def convert_image(source: Path) -> Path:
    if source.suffix.lower() == ".webp":
        return source

    destination = source.with_suffix(".webp")
    with Image.open(source) as image:
        image.load()
        if image.width > MAX_WIDTH:
            height = round(image.height * MAX_WIDTH / image.width)
            image = image.resize((MAX_WIDTH, height), Image.Resampling.LANCZOS)

        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")

        image.save(destination, "WEBP", quality=QUALITY, method=6)

    return destination


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    original_size = sum(
        path.stat().st_size
        for root in IMAGE_ROOTS
        for path in root.rglob("*")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    replacements = 0

    for root in IMAGE_ROOTS:
        for source in sorted(root.rglob("*")):
            if source.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue
            destination = convert_image(source)
            old_ref = source.relative_to(PROJECT_ROOT).as_posix()
            new_ref = destination.relative_to(PROJECT_ROOT).as_posix()
            if old_ref in html:
                html = html.replace(old_ref, new_ref)
                replacements += 1

    INDEX_PATH.write_text(html, encoding="utf-8", newline="\n")
    referenced_webp_size = sum(
        path.stat().st_size
        for root in IMAGE_ROOTS
        for path in root.rglob("*.webp")
        if path.relative_to(PROJECT_ROOT).as_posix() in html
    )
    print(
        f"Updated {replacements} image references. "
        f"Original image library: {original_size / 1024 / 1024:.2f} MB; "
        f"referenced WebP assets: {referenced_webp_size / 1024 / 1024:.2f} MB."
    )


if __name__ == "__main__":
    main()
