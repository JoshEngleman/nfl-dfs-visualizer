#!/usr/bin/env python3
"""
Compress headshot images for web use.
Reduces file sizes from ~5MB to ~50-100KB while maintaining quality.
"""

import os
from pathlib import Path
from PIL import Image

def compress_headshots(input_dir, output_dir, max_size=400, quality=85):
    """
    Compress headshot images for web use.

    Args:
        input_dir: Directory containing original headshots
        output_dir: Directory to save compressed headshots
        max_size: Maximum width/height in pixels (default 400)
        quality: JPEG quality 1-100 (default 85, higher = better quality)
    """

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Get all PNG files
    png_files = list(input_path.glob('*.png'))

    if not png_files:
        print(f"ERROR: No PNG files found in {input_dir}")
        return

    print(f"Found {len(png_files)} images to compress")
    print(f"Settings: max_size={max_size}px, quality={quality}")
    print(f"Output: {output_path.absolute()}\n")

    total_original_size = 0
    total_compressed_size = 0
    processed = 0
    failed = 0

    for img_file in png_files:
        try:
            # Get original file size
            original_size = img_file.stat().st_size
            total_original_size += original_size

            # Open image
            img = Image.open(img_file)

            # Convert RGBA to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            # Resize if needed (maintain aspect ratio)
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            # Save as optimized PNG or JPEG
            output_file = output_path / img_file.name

            # Try PNG first with optimization
            img.save(output_file, 'PNG', optimize=True)

            # If still too large, convert to JPEG
            compressed_size = output_file.stat().st_size
            if compressed_size > 200_000:  # If larger than 200KB
                # Save as JPEG instead
                output_file = output_path / img_file.stem
                output_file = output_file.with_suffix('.png')  # Keep .png extension for compatibility
                img.save(output_file, 'JPEG', quality=quality, optimize=True)
                compressed_size = output_file.stat().st_size

            total_compressed_size += compressed_size

            # Calculate savings
            reduction = ((original_size - compressed_size) / original_size) * 100

            processed += 1
            if processed % 25 == 0:
                print(f"  Processed {processed}/{len(png_files)}...")

        except Exception as e:
            print(f"  ❌ Failed to process {img_file.name}: {e}")
            failed += 1

    # Summary
    print(f"\n✅ Compression complete!")
    print(f"   Processed: {processed} images")
    print(f"   Failed: {failed} images")
    print(f"   Original size: {total_original_size / 1_000_000:.1f} MB")
    print(f"   Compressed size: {total_compressed_size / 1_000_000:.1f} MB")
    print(f"   Savings: {((total_original_size - total_compressed_size) / total_original_size * 100):.1f}%")
    print(f"   Average per image: {total_compressed_size / processed / 1000:.1f} KB")
    print(f"\nCompressed images saved to: {output_path.absolute()}")

if __name__ == '__main__':
    # Configuration
    input_dir = 'headshot_cache'
    output_dir = 'headshot_cache_compressed'
    max_size = 400  # 400x400 pixels max
    quality = 85    # JPEG quality (85 is good balance)

    print("=" * 60)
    print("Headshot Image Compression Tool")
    print("=" * 60)
    print()

    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"ERROR: {input_dir} not found")
        print(f"Current directory: {os.getcwd()}")
        exit(1)

    # Run compression
    compress_headshots(input_dir, output_dir, max_size, quality)

    print("\nNext step: Upload compressed images to GoDaddy at /nfl-dfs/headshots/")
