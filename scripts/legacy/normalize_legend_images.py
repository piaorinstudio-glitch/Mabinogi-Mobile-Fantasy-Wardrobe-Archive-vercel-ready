"""Create consistently framed transparent four-character catalogue images."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "assets" / "normalized"
CANVAS_SIZE = (1600, 1080)
CONTENT_HEIGHT = 952
TOP_MARGIN = 64
CORRECTED_LEGEND_NAMES = {
    "03_holy_lucete_regular.webp": "03_holy_lucete_hooded.webp",
    "03_holy_lucete_hooded.webp": "03_holy_lucete_regular.webp",
    "04_frost_haven_regular.webp": "04_frost_haven_hooded.webp",
    "04_frost_haven_hooded.webp": "04_frost_haven_regular.webp",
}


def normalize(source: Path, target: Path) -> None:
    image = Image.open(source).convert("RGBA")
    bounds = image.getchannel("A").getbbox()
    if not bounds:
        raise ValueError(f"No visible pixels found in {source.name}")

    cropped = image.crop(bounds)
    scale = CONTENT_HEIGHT / cropped.height
    width = round(cropped.width * scale)
    resized = cropped.resize((width, CONTENT_HEIGHT), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((CANVAS_SIZE[0] - width) // 2, TOP_MARGIN))
    canvas.save(target, "WEBP", quality=92, method=4)


def main() -> None:
    groups = {
        "legend": sorted((ROOT / "assets" / "legend").glob("*.webp")),
        "abyss": sorted((ROOT / "image").glob("abyss-*.webp")),
        "raid": sorted((ROOT / "image").glob("raid-*.webp")),
    }
    for group, sources in groups.items():
        output_dir = OUTPUT_ROOT / group
        output_dir.mkdir(parents=True, exist_ok=True)
        for source in sources:
            alpha = Image.open(source).convert("RGBA").getchannel("A")
            if alpha.getextrema()[0] == 255:
                continue
            target_name = CORRECTED_LEGEND_NAMES.get(source.name, source.name) if group == "legend" else source.name
            normalize(source, output_dir / target_name)
            print(f"normalized {group}/{target_name}")

    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")
    replacements = {
        '"assets/legend/': '"assets/normalized/legend/',
        '"image/abyss-3.webp"': '"assets/normalized/abyss/abyss-3.webp"',
        '"image/raid-3.webp"': '"assets/normalized/raid/raid-3.webp"',
        '"image/raid-4.webp"': '"assets/normalized/raid/raid-4.webp"',
        '"image/raid-5.webp"': '"assets/normalized/raid/raid-5.webp"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    index_path.write_text(html, encoding="utf-8")
    print("updated index.html image references")


if __name__ == "__main__":
    main()
