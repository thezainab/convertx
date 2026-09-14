from PIL import Image
from app.services.conversion_registry import registry

def convert_image(input_path: str, output_path: str, target_format: str) -> bool:
    try:
        with Image.open(input_path) as img:
            # Agar hum PNG (jisme transparent background hota hai) se JPG mein convert kar rahe hain,
            # to background ko pehle RGB mein badalna zaroori hai warna error aayega.
            if target_format.upper() in ['JPEG', 'JPG'] and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # File ko naye format mein save karo
            img.save(output_path, format=target_format.upper())
        return True
    except Exception as e:
        print(f"Image conversion fail ho gayi: {e}")
        return False

# Ab hum apni registry ko batayenge ke konsi conversion is function se karni hai
registry.register('jpg', 'png', lambda i, o: convert_image(i, o, 'PNG'))
registry.register('jpeg', 'png', lambda i, o: convert_image(i, o, 'PNG'))
registry.register('png', 'jpg', lambda i, o: convert_image(i, o, 'JPEG'))
registry.register('png', 'jpeg', lambda i, o: convert_image(i, o, 'JPEG'))
registry.register('webp', 'jpg', lambda i, o: convert_image(i, o, 'JPEG'))
registry.register('jpg', 'webp', lambda i, o: convert_image(i, o, 'WEBP'))
registry.register('png', 'webp', lambda i, o: convert_image(i, o, 'WEBP'))