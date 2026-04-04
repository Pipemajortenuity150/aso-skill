#!/usr/bin/env python3
"""
App Store Screenshot Composer

Composites headline text, device frame template, and app screenshot
into a pixel-perfect App Store Connect image.

Based on adamlyttleapps/claude-skill-aso-appstore-screenshots

Usage:
    python3 screenshot_composer.py \
        --bg "#E31837" \
        --verb "TRACK" \
        --desc "TRADING CARD PRICES" \
        --screenshot path/to/simulator.png \
        --output output.png

Requirements:
    pip install Pillow
    SF Pro Display Black font at /Library/Fonts/SF-Pro-Display-Black.otf
"""

import argparse
import os
from typing import Tuple, List, Optional
from dataclasses import dataclass

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


# ── Canvas Dimensions ──────────────────────────────────────────────────
DIMENSIONS = {
    "6.5": (1242, 2688),  # iPhone 6.5"
    "6.7": (1290, 2796),  # iPhone 6.7" (default)
    "6.9": (1320, 2868),  # iPhone 6.9"
}

DEFAULT_SIZE = "6.7"

# ── Device Frame Constants ─────────────────────────────────────────────
DEVICE_W = 1030
BEZEL = 15
SCREEN_W = DEVICE_W - 2 * BEZEL  # 1000
SCREEN_CORNER_R = 62

# ── Layout ─────────────────────────────────────────────────────────────
DEVICE_Y = 720  # Device top position (fixed)
TEXT_TOP = 200  # Text starts at this Y position

# ── Typography ─────────────────────────────────────────────────────────
VERB_SIZE_MAX = 256
VERB_SIZE_MIN = 150
DESC_SIZE = 124
VERB_DESC_GAP = 20
DESC_LINE_GAP = 24

# Font paths (in order of preference)
FONT_PATHS = [
    "/Library/Fonts/SF-Pro-Display-Black.otf",
    "/System/Library/Fonts/SFPro-Display-Black.otf",
    "/Library/Fonts/Arial Black.ttf",
]


@dataclass
class ScreenshotConfig:
    """Configuration for screenshot generation."""
    bg_color: str  # Hex color like "#E31837"
    verb: str  # Action verb like "TRACK"
    desc: str  # Benefit descriptor like "TRADING CARD PRICES"
    screenshot_path: str  # Path to simulator screenshot
    output_path: str  # Where to save result
    display_size: str = "6.7"  # Display size key


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def find_font() -> Optional[str]:
    """Find available font path."""
    for path in FONT_PATHS:
        if os.path.exists(path):
            return path
    return None


def word_wrap(draw: ImageDraw, text: str, font: ImageFont, max_w: int) -> List[str]:
    """Wrap text to fit within max width."""
    words = text.split()
    lines, current = [], ""

    for word in words:
        test = f"{current} {word}".strip()
        if draw.textlength(test, font=font) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def fit_font(text: str, max_w: int, size_max: int, size_min: int, font_path: str) -> ImageFont:
    """Return the largest font size where text fits within max_w."""
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    for size in range(size_max, size_min - 1, -4):
        font = ImageFont.truetype(font_path, size)
        bbox = dummy.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_w:
            return font

    return ImageFont.truetype(font_path, size_min)


def draw_centered_text(
    draw: ImageDraw,
    canvas_w: int,
    y: int,
    text: str,
    font: ImageFont,
    max_w: int = None
) -> int:
    """Draw centered text, return new Y position."""
    lines = word_wrap(draw, text, font, max_w) if max_w else [text]

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        h = bbox[3] - bbox[1]
        # Use anchor="mt" (middle-top) for horizontal centering
        draw.text(
            (canvas_w // 2, y - bbox[1]),
            line,
            fill="white",
            font=font,
            anchor="mt"
        )
        y += h + DESC_LINE_GAP

    return y


def generate_device_frame(width: int, height: int) -> Image:
    """Generate a simple device frame (black rounded rectangle with transparent screen)."""
    # Create transparent image
    frame = Image.new("RGBA", (DEVICE_W, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame)

    # Device body (black rounded rectangle)
    device_radius = 80
    draw.rounded_rectangle(
        [0, 0, DEVICE_W, height],
        radius=device_radius,
        fill=(20, 20, 20, 255)  # Near-black
    )

    # Screen cutout (transparent)
    screen_rect = [BEZEL, BEZEL, DEVICE_W - BEZEL, height - BEZEL]
    draw.rounded_rectangle(
        screen_rect,
        radius=SCREEN_CORNER_R,
        fill=(0, 0, 0, 0)
    )

    # Dynamic Island
    island_w, island_h = 200, 50
    island_x = (DEVICE_W - island_w) // 2
    island_y = BEZEL + 20
    draw.rounded_rectangle(
        [island_x, island_y, island_x + island_w, island_y + island_h],
        radius=island_h // 2,
        fill=(20, 20, 20, 255)
    )

    # Side buttons (power button on right)
    button_w, button_h = 6, 100
    draw.rounded_rectangle(
        [DEVICE_W - 3, 300, DEVICE_W + 3, 300 + button_h],
        radius=3,
        fill=(40, 40, 40, 255)
    )

    # Volume buttons on left
    draw.rounded_rectangle(
        [-3, 280, 3, 280 + 60],
        radius=3,
        fill=(40, 40, 40, 255)
    )
    draw.rounded_rectangle(
        [-3, 360, 3, 360 + 60],
        radius=3,
        fill=(40, 40, 40, 255)
    )

    return frame


def compose_screenshot(config: ScreenshotConfig) -> bool:
    """
    Compose an App Store screenshot.

    Returns True on success, False on failure.
    """
    if not HAS_PILLOW:
        print("Error: Pillow not installed. Run: pip install Pillow")
        return False

    font_path = find_font()
    if not font_path:
        print("Error: No suitable font found. Install SF Pro Display Black.")
        return False

    # Get dimensions
    canvas_w, canvas_h = DIMENSIONS.get(config.display_size, DIMENSIONS[DEFAULT_SIZE])
    max_text_w = int(canvas_w * 0.92)
    max_verb_w = int(canvas_w * 0.92)

    bg = hex_to_rgb(config.bg_color)

    # ── 1. Create Canvas ───────────────────────────────────────────────
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (*bg, 255))
    draw = ImageDraw.Draw(canvas)

    # ── 2. Load Fonts ──────────────────────────────────────────────────
    verb_font = fit_font(
        config.verb.upper(),
        max_verb_w,
        VERB_SIZE_MAX,
        VERB_SIZE_MIN,
        font_path
    )
    desc_font = ImageFont.truetype(font_path, DESC_SIZE)

    # ── 3. Draw Text ───────────────────────────────────────────────────
    y = TEXT_TOP
    y = draw_centered_text(draw, canvas_w, y, config.verb.upper(), verb_font)
    y += VERB_DESC_GAP
    draw_centered_text(draw, canvas_w, y, config.desc.upper(), desc_font, max_w=max_text_w)

    # ── 4. Calculate Positions ─────────────────────────────────────────
    device_x = (canvas_w - DEVICE_W) // 2
    device_y = DEVICE_Y
    screen_x = device_x + BEZEL
    screen_y = device_y + BEZEL
    screen_h = canvas_h - screen_y + 500  # Extends beyond canvas

    # ── 5. Load and Place Screenshot ───────────────────────────────────
    try:
        shot = Image.open(config.screenshot_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading screenshot: {e}")
        return False

    # Scale to fill screen width
    scale = SCREEN_W / shot.width
    sc_w = SCREEN_W
    sc_h = int(shot.height * scale)
    shot = shot.resize((sc_w, sc_h), Image.LANCZOS)

    # Create screen mask (rounded rectangle)
    scr_mask = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(scr_mask).rounded_rectangle(
        [screen_x, screen_y, screen_x + SCREEN_W, screen_y + screen_h],
        radius=SCREEN_CORNER_R,
        fill=255,
    )

    # Black screen background + screenshot
    scr_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(scr_layer).rounded_rectangle(
        [screen_x, screen_y, screen_x + SCREEN_W, screen_y + screen_h],
        radius=SCREEN_CORNER_R,
        fill=(0, 0, 0, 255),
    )
    scr_layer.paste(shot, (screen_x, screen_y))
    scr_layer.putalpha(scr_mask)

    canvas = Image.alpha_composite(canvas, scr_layer)

    # ── 6. Add Device Frame ────────────────────────────────────────────
    frame = generate_device_frame(DEVICE_W, canvas_h - device_y + 100)
    frame_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    frame_layer.paste(frame, (device_x, device_y))
    canvas = Image.alpha_composite(canvas, frame_layer)

    # ── 7. Save ────────────────────────────────────────────────────────
    # Ensure output directory exists
    output_dir = os.path.dirname(config.output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    canvas.convert("RGB").save(config.output_path, "PNG")
    print(f"✓ {config.output_path} ({canvas_w}×{canvas_h})")

    return True


def crop_to_app_store_dimensions(
    input_path: str,
    output_path: str,
    target_w: int = 1290,
    target_h: int = 2796
) -> bool:
    """
    Crop and resize image to exact App Store Connect dimensions.

    This handles the aspect ratio mismatch when AI generates at 9:16
    but App Store needs narrower ratio (~0.461).
    """
    if not HAS_PILLOW:
        return False

    try:
        img = Image.open(input_path)
        w, h = img.size

        # Calculate crop width to match target aspect ratio
        target_ratio = target_w / target_h
        current_ratio = w / h

        if current_ratio > target_ratio:
            # Image is wider than target - crop sides
            crop_w = int(h * target_ratio)
            offset_x = (w - crop_w) // 2
            img = img.crop((offset_x, 0, offset_x + crop_w, h))

        # Resize to exact dimensions
        img = img.resize((target_w, target_h), Image.LANCZOS)
        img.save(output_path, "JPEG", quality=95)

        print(f"✓ Cropped to {target_w}×{target_h}: {output_path}")
        return True

    except Exception as e:
        print(f"Error cropping image: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Compose App Store screenshot"
    )
    parser.add_argument(
        "--bg", required=True,
        help="Background hex colour (#E31837)"
    )
    parser.add_argument(
        "--verb", required=True,
        help="Action verb (TRACK)"
    )
    parser.add_argument(
        "--desc", required=True,
        help="Benefit descriptor (TRADING CARD PRICES)"
    )
    parser.add_argument(
        "--screenshot", required=True,
        help="Simulator screenshot path"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--size", default="6.7",
        choices=["6.5", "6.7", "6.9"],
        help="Display size (default: 6.7)"
    )

    args = parser.parse_args()

    config = ScreenshotConfig(
        bg_color=args.bg,
        verb=args.verb,
        desc=args.desc,
        screenshot_path=args.screenshot,
        output_path=args.output,
        display_size=args.size,
    )

    success = compose_screenshot(config)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
