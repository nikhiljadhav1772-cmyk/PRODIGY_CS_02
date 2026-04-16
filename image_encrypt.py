from PIL import Image
import os

def encrypt_image(image_path, key):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # XOR each channel with key and shift values
            new_r = (r ^ key) % 256
            new_g = (g ^ (key + 1)) % 256
            new_b = (b ^ (key + 2)) % 256
            pixels[x, y] = (new_r, new_g, new_b)

    # Swap pixels: swap (x, y) with (width-1-x, height-1-y)
    for y in range(height // 2):
        for x in range(width):
            pixels[x, y], pixels[width - 1 - x, height - 1 - y] = \
                pixels[width - 1 - x, height - 1 - y], pixels[x, y]

    base, ext = os.path.splitext(image_path)
    output_path = base + "_encrypted" + ext
    img.save(output_path)
    print(f"\n[+] Image encrypted successfully!")
    print(f"    Saved as: {output_path}")
    return output_path


def decrypt_image(image_path, key):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # Reverse the pixel swap first
    for y in range(height // 2):
        for x in range(width):
            pixels[x, y], pixels[width - 1 - x, height - 1 - y] = \
                pixels[width - 1 - x, height - 1 - y], pixels[x, y]

    # Reverse XOR (XOR with same key reverses itself)
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            orig_r = (r ^ key) % 256
            orig_g = (g ^ (key + 1)) % 256
            orig_b = (b ^ (key + 2)) % 256
            pixels[x, y] = (orig_r, orig_g, orig_b)

    base, ext = os.path.splitext(image_path)
    # Remove "_encrypted" from name if present
    if base.endswith("_encrypted"):
        base = base[: -len("_encrypted")]
    output_path = base + "_decrypted" + ext
    img.save(output_path)
    print(f"\n[+] Image decrypted successfully!")
    print(f"    Saved as: {output_path}")
    return output_path


def main():
    print("=" * 45)
    print("      IMAGE ENCRYPTION TOOL")
    print("      (Pixel Manipulation Method)")
    print("=" * 45)

    print("\nChoose mode:")
    print("1. Encrypt an image")
    print("2. Decrypt an image")

    while True:
        choice = input("\nEnter choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            break
        print("Invalid. Enter 1 or 2.")

    image_path = input("Enter image file path (e.g. photo.png): ").strip()

    if not os.path.exists(image_path):
        print(f"[!] File not found: {image_path}")
        return

    while True:
        try:
            key = int(input("Enter encryption key (0-255): ").strip())
            if 0 <= key <= 255:
                break
            print("Key must be between 0 and 255.")
        except ValueError:
            print("Invalid. Enter a number.")

    print("\nProcessing... please wait.")

    if choice == "1":
        encrypt_image(image_path, key)
    else:
        decrypt_image(image_path, key)

    print("\nDone!")


if __name__ == "__main__":
    main()
