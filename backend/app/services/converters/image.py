from PIL import Image, ImageOps
from app.services.conversion_registry import registry


def convert_image(input_path: str, output_path: str, target_format: str) -> bool:
    try:
        with Image.open(input_path) as img:
            # Phone ki photos ki rotation (EXIF) theek karo
            img = ImageOps.exif_transpose(img)

            fmt = target_format.upper()

            # JPEG mein transparency nahi hoti, is liye safed background par rakho
            if fmt in ('JPEG', 'JPG'):
                fmt = 'JPEG'
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

            img.save(output_path, format=fmt)
        return True
    except Exception as e:
        print(f"Image conversion fail ho gayi: {e}")
        return False


def _make(fmt: str):
    return lambda i, o: convert_image(i, o, fmt)


# Source formats jo input ho sakte hain
_SOURCES = ['jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif']
# Target format -> PIL ka format naam
_TARGETS = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'webp': 'WEBP',
}

for src in _SOURCES:
    for tgt, pil_fmt in _TARGETS.items():
        # Same format se same format ki conversion ki zaroorat nahi
        if src == tgt:
            continue
        registry.register(src, tgt, _make(pil_fmt))