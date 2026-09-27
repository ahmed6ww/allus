---
name: allus
description: Allus plans and generates hand-drawn, absurd but clean 16:9 article illustrations starring Xiaohei, a deadpan small black character who performs the core action. Use when the user asks for article illustrations, blog post images, inline explainer images, hand-drawn or sketch-style illustrations, visualizing a concept, workflow, process, structure, state, or metaphor, a shot list or illustration plan for an article, or editing or removing text or a title from a generated illustration, or mentions Allus. Works for articles in any language (English, Chinese, Urdu and more); labels follow the article language and default to English. Also triggers on 配图, 正文配图, 小黑. Pure white background, black line art, sparse red/orange/blue handwritten labels, lots of white space, one idea per image.
---

# Allus: Absurd Article Illustrations

## Purpose

Design and generate 16:9 horizontal inline illustrations for articles. The goal is not commercial illustration, PPT infographics, or cute cartoons. The goal is to turn a key judgment, process, structure, state, or metaphor from the article into a clean, absurd, creative hand-drawn explainer that is readable but never an instruction manual.

The default visual character is Xiaohei: solid black, white dot eyes, thin legs, blank expression, seriously doing something absurd but valid. The character must take part in the core action of the image, never just stand beside it as decoration.

## Read these references first

Read them as the task needs them. Do not load everything at once:

- `references/language.md`: which language the labels use, how many, how long, lettering style, no-text mode, and what to do when text comes out garbled. Read this first.
- `references/style-dna.md`: style DNA, colors, text, forbidden list.
- `references/character.md`: the character's appearance, personality, action library, and forbidden list.
- `references/composition-patterns.md`: structure types, the original metaphor method, and anti-copy rules.
- `references/prompt-template.md`: the single-image prompt template.
- `references/qa-checklist.md`: post-generation checks and iteration rules.
- `assets/examples/`: only for occasional visual calibration, not part of the default generation path. Never copy their compositions, objects, or labels.

## Workflow

### 1. Digest the article

Read the article, link, Notion page, Markdown file, or screenshot the user provides. Extract:

- The core argument.
- Which paragraphs carry a cognitive turn.
- Which content is worth explaining with an image.
- Which parts work better as text only and need no image.

Do not spread images evenly. Prioritize "cognitive anchors": the core judgment, two breakpoints, an input-output loop, a split, a before/after contrast, one source reused many ways, a handoff path, common pitfalls, a change in someone's state.

Resolve the label language now, following `references/language.md`.

### 2. Plan the illustrations first

If the user only asks to analyze where images should go, output a shot list first. For each image give:

- Placement (after which paragraph)
- Theme
- Core idea
- Structure type
- What the character is doing
- Suggested elements
- Suggested labels in the resolved language (or "no text")

Default to 4 to 8 images. For short pieces, 1 to 3. Even long articles rarely need more than 9. Enough is enough; do not turn the article into a picture book.

### 3. Generate each image separately

If the user explicitly says generate, output, make the images, or similar, do not stop to confirm. Just generate.

Run `uv run ~/.claude/skills/allus/scripts/gen_image.py --prompt "<full prompt>" --out assets/<article-slug>-illustrations/NN-name.png` once per image. For edits add `--edit <existing.png>`. If text comes out garbled, follow the text failure handling in references/language.md.

The script picks the backend automatically: Gemini when `GEMINI_API_KEY` is set, OpenAI when only `OPENAI_API_KEY` is set, or whatever `ALLUS_IMAGE_PROVIDER` says. Add `--provider openai` or `--provider gemini` to force one.

Never combine several images into one. Each image explains only one core structure. Build every prompt from `references/prompt-template.md`. It must include:

- 16:9 horizontal article illustration
- Pure white background
- Black hand-drawn line art
- Sparse red/orange/blue handwritten labels in the resolved language, or no text
- Lots of white space
- The character as the subject of the core action, described by appearance only, never by name
- No PPT, no commercial illustration, nothing childish or cute, no complex architecture, no type title in the top-left corner

Do not copy past examples. Examples only show style density and how the character takes part. Do not reuse known compositions such as the conveyor belt with breakpoints, the character pulling lines, the material fish, the stamping toolbox, or the pitfall path, unless the user explicitly asks to copy a specific image. Invent a strange but valid metaphor from the current article every time.

### 4. Check and iterate

After generating, open each image and check it against `references/qa-checklist.md`. If any of these appear, regenerate or do a local edit:

- The character is only decoration
- The image is too crowded
- It looks like a flowchart or PPT
- Too much text, misspelled text, or text that was not in the label list
- A title such as "Common Pitfalls / Flowchart / System Architecture" in the top-left corner
- The style is too cute, childish, or rigid
- The background is not clean white

### 5. Save and deliver

If the user is working in a workspace, save the final images to:

```text
assets/<article-slug>-illustrations/
```

Name them in order:

```text
01-topic-name.png
02-topic-name.png
```

Keep the original generated files. Never overwrite existing assets unless the user explicitly asks to replace them. The script adds a `-v2` suffix instead of overwriting.

## Output

Keep the planning output short and precise. The delivery report after generating includes:

- How many images were generated
- The purpose of each image
- Save paths
- Which images are strongest and which are optional
- Total images generated, including retries

Do not write long explanations of the style theory. Let the images speak.

---

Allus is adapted from Ian Xiaohei Illustrations by Ian (github.com/helloianneo), MIT License. Language-agnostic version with a Gemini or OpenAI backend for Claude Code.
