#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "openai", "pillow"]
# ///
"""Image backend for the ian-xiaohei-illustrations skill in Claude Code.

Replaces Codex's built-in image_gen tool with either Gemini (Nano Banana, via
the Interactions API) or OpenAI (gpt-image, via the Images API).

Generate:
  uv run gen_image.py --prompt "..." --out assets/my-post-illustrations/01-trust-bridge.png

Edit an existing image (e.g. remove a stray title):
  uv run gen_image.py --edit assets/my-post-illustrations/01-trust-bridge.png \
      --prompt "Remove the title in the top-left corner, keep everything else unchanged" \
      --out assets/my-post-illustrations/01-trust-bridge.png

Providers (--provider, or the XIAOHEI_IMAGE_PROVIDER environment variable):
  gemini   needs GEMINI_API_KEY. Default when GEMINI_API_KEY is set.
  openai   needs OPENAI_API_KEY. Default when only OPENAI_API_KEY is set.

Gemini models:
  gemini-3.1-flash-image       Nano Banana 2 (default, good text rendering, fast)
  gemini-3-pro-image           Nano Banana Pro (--pro, best for dense or Chinese text)
  gemini-3.1-flash-lite-image  Nano Banana 2 Lite (cheapest, 1K only)

OpenAI models:
  gpt-image-1.5                default; --quality low / medium / high
  OpenAI renders landscape at 1536x1024 (3:2). The result is padded with
  white to the requested aspect ratio, so nothing is cropped.

Requires: uv (dependencies install automatically from the header above).
"""

import argparse
import base64
import io
import mimetypes
import os
import sys
from pathlib import Path

from PIL import Image

DEFAULT_MODEL = "gemini-3.1-flash-image"
PRO_MODEL = "gemini-3-pro-image"
OPENAI_MODEL = "gpt-image-1.5"


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


def default_provider() -> str:
    env = os.environ.get("XIAOHEI_IMAGE_PROVIDER", "").strip().lower()
    if env in ("gemini", "openai"):
        return env
    if not os.environ.get("GEMINI_API_KEY") and os.environ.get("OPENAI_API_KEY"):
        return "openai"
    return "gemini"


def parse_aspect(aspect: str) -> float:
    w, h = aspect.split(":")
    return float(w) / float(h)


def pad_to_aspect(img: Image.Image, aspect: str) -> Image.Image:
    """Pad with white (the style's background) to reach the aspect ratio."""
    target = parse_aspect(aspect)
    w, h = img.size
    if abs(w / h - target) < 0.01:
        new_w, new_h = w, h
    elif w / h < target:
        new_w, new_h = round(h * target), h
    else:
        new_w, new_h = w, round(w / target)
    canvas = Image.new("RGB", (new_w, new_h), "white")
    # Composite over white: dropping alpha would expose the color data under
    # transparent pixels as a dark, glowing background.
    rgba = img.convert("RGBA")
    canvas.paste(rgba, ((new_w - w) // 2, (new_h - h) // 2), mask=rgba)
    return canvas


def run_gemini(args) -> tuple[bytes | None, str]:
    from google import genai

    model = PRO_MODEL if args.pro else (args.model or DEFAULT_MODEL)
    size = "1K" if "lite" in model else args.size  # Lite only supports 1K

    if args.edit:
        src = Path(args.edit)
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
    label = f"gemini {model}, {args.aspect}, {size}"
    if not image or not image.data:
        # Usually a safety block or the model replying with text only
        if interaction.output_text:
            print(f"Model said: {interaction.output_text}", file=sys.stderr)
        return None, label
    return base64.b64decode(image.data), label


def run_openai(args) -> tuple[bytes | None, str]:
    from openai import OpenAI

    model = args.model or OPENAI_MODEL
    ratio = parse_aspect(args.aspect)
    size = "1536x1024" if ratio > 1.05 else "1024x1536" if ratio < 0.95 else "1024x1024"

    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    common = {"model": model, "prompt": args.prompt, "size": size, "quality": args.quality,
              "background": "opaque", "n": 1}
    if args.edit:
        with open(args.edit, "rb") as f:
            result = client.images.edit(image=f, **common)
    else:
        result = client.images.generate(**common)

    label = f"openai {model}, {size} padded to {args.aspect}, quality={args.quality}"
    if not result.data or not result.data[0].b64_json:
        return None, label
    return base64.b64decode(result.data[0].b64_json), label


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or edit one xiaohei illustration with Gemini or OpenAI.")
    parser.add_argument("--prompt", required=True, help="Full image prompt")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--edit", help="Existing image to edit instead of generating from scratch")
    parser.add_argument("--provider", choices=["gemini", "openai"], default=default_provider(),
                        help="Image backend (default: XIAOHEI_IMAGE_PROVIDER, else whichever API key is set)")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio, default 16:9")
    parser.add_argument("--size", default="2K", choices=["512px", "1K", "2K", "4K"],
                        help="Gemini resolution (uppercase K required by the API)")
    parser.add_argument("--quality", default="medium", choices=["low", "medium", "high", "auto"],
                        help="OpenAI quality, default medium")
    parser.add_argument("--model", help=f"Override the model (defaults: {DEFAULT_MODEL}, {OPENAI_MODEL})")
    parser.add_argument("--pro", action="store_true", help=f"Gemini only: shortcut for --model {PRO_MODEL}")
    parser.add_argument("--think", action="store_true",
                        help="Gemini Flash only: thinking_level=high, slower, better composition")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing file")
    args = parser.parse_args()

    if args.edit and not Path(args.edit).exists():
        print(f"Edit source not found: {args.edit}", file=sys.stderr)
        return 1

    key = "OPENAI_API_KEY" if args.provider == "openai" else "GEMINI_API_KEY"
    if not os.environ.get(key):
        print(f"{key} is not set (provider={args.provider}).", file=sys.stderr)
        return 1

    run = run_openai if args.provider == "openai" else run_gemini
    data, label = run(args)
    if data is None:
        print(f"No image returned ({label}).", file=sys.stderr)
        return 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not args.overwrite:
        out = unique_path(out)

    pad_to_aspect(Image.open(io.BytesIO(data)), args.aspect).save(out, format="PNG")
    print(f"Saved: {out.resolve()}  ({label})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
