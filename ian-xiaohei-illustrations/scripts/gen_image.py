#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "pillow"]
# ///
"""Gemini image backend for the ian-xiaohei-illustrations skill in Claude Code.

Replaces Codex's built-in image_gen tool with Gemini (Nano Banana) via the
Interactions API.

Generate:
  uv run gen_image.py --prompt "..." --out assets/my-post-illustrations/01-trust-bridge.png

Edit an existing image (e.g. remove a stray title):
  uv run gen_image.py --edit assets/my-post-illustrations/01-trust-bridge.png \
      --prompt "Remove the title in the top-left corner, keep everything else unchanged" \
      --out assets/my-post-illustrations/01-trust-bridge.png

Models:
  gemini-3.1-flash-image       Nano Banana 2 (default, good text rendering, fast)
  gemini-3-pro-image           Nano Banana Pro (--pro, best for dense or Chinese text)
  gemini-3.1-flash-lite-image  Nano Banana 2 Lite (cheapest, 1K only)

Requires: uv (dependencies install automatically from the header above),
and GEMINI_API_KEY set in the environment.
"""

import argparse
import base64
import io
import mimetypes
import sys
from pathlib import Path

from google import genai
from PIL import Image

DEFAULT_MODEL = "gemini-3.1-flash-image"
PRO_MODEL = "gemini-3-pro-image"


def unique_path(path: Path) -> Path:
    """Never overwrite existing assets (the skill's own rule)."""
    if not path.exists():
        return path
    stem, suffix, n = path.stem, path.suffix, 2
    while True:
        candidate = path.with_name(f"{stem}-v{n}{suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or edit one xiaohei illustration with Gemini.")
    parser.add_argument("--prompt", required=True, help="Full image prompt")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--edit", help="Existing image to edit instead of generating from scratch")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio, default 16:9")
    parser.add_argument("--size", default="2K", choices=["512px", "1K", "2K", "4K"],
                        help="Resolution (uppercase K required by the API)")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--pro", action="store_true", help=f"Shortcut for --model {PRO_MODEL}")
    parser.add_argument("--think", action="store_true",
                        help="thinking_level=high (Flash models only): slower, better composition")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing file")
    args = parser.parse_args()

    model = PRO_MODEL if args.pro else args.model
    size = "1K" if "lite" in model else args.size  # Lite only supports 1K

    if args.edit:
        src = Path(args.edit)
        if not src.exists():
            print(f"Edit source not found: {src}", file=sys.stderr)
            return 1
        mime = mimetypes.guess_type(src.name)[0] or "image/png"
        model_input = [
            {"type": "text", "text": args.prompt},
            {
                "type": "image",
                "data": base64.b64encode(src.read_bytes()).decode("utf-8"),
                "mime_type": mime,
            },
        ]
    else:
        model_input = args.prompt

    kwargs = {
        "model": model,
        "input": model_input,
        "response_format": {
            "type": "image",
            "mime_type": "image/jpeg",  # the API only returns JPEG; converted to PNG on save
            "aspect_ratio": args.aspect,
            "image_size": size,
        },
    }
    if args.think and "pro" not in model:
        kwargs["generation_config"] = {"thinking_level": "high"}

    client = genai.Client()  # reads GEMINI_API_KEY from the environment
    interaction = client.interactions.create(**kwargs)

    image = interaction.output_image
    if not image or not image.data:
        # Usually a safety block or the model replying with text only
        print("No image returned.", file=sys.stderr)
        if interaction.output_text:
            print(f"Model said: {interaction.output_text}", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not args.overwrite:
        out = unique_path(out)

    Image.open(io.BytesIO(base64.b64decode(image.data))).save(out, format="PNG")
    print(f"Saved: {out.resolve()}  (model={model}, {args.aspect}, {size})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
