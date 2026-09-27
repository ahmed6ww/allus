# Language

This file is the single source of truth for annotation language. Every other file points here instead of naming a language.

## 1. Resolution order

The annotation language for an image is decided in this order:

1. Explicit user request ("Urdu labels", "Chinese labels", "no text").
2. The language of the article or text the user provided.
3. English, when there is no article or the language is unclear.

The shot list, the planning output, and the labels all use the resolved language. The language the user chats in does not change the label language unless the user asks for it.

## 2. Per-language rules

| Language | Labels per image | Label length | Lettering style for the prompt | Model advice |
|---|---|---|---|---|
| English | 3 to 5 | 1 to 3 words | casual lowercase marker handwriting, slightly uneven, like quick notes on a whiteboard sketch | default Flash model is enough |
| Chinese | 5 to 8 | 2 to 8 characters | casual Chinese handwriting with a marker, slightly uneven | retry with `--pro` if characters are garbled |
| Urdu / Arabic (RTL scripts) | 0 to 3 | 1 to 2 words | casual handwritten script, right-to-left | warn the user that RTL text rendering is unreliable, recommend no-text mode and captions in the post instead |
| Other languages | 3 to 5 | shortest natural phrase | casual handwriting in that script | retry with `--pro` if text is garbled |
| No-text mode | 0 | none | none | any model |

Why the counts differ: two Chinese characters can carry a whole concept, while English needs more words and roughly three times the horizontal space. English gets fewer labels so the image keeps at least 35% white space.

When filling `references/prompt-template.md`, `{LANGUAGE}` is the resolved language name and `{LETTERING}` is the lettering style from this table.

## 3. No-text mode

When no-text mode is active, the image prompt must say:

"No text, letters, numbers, or labels anywhere in the image. Communicate only through the drawing."

Color rules still apply to arrows and marks.

## 4. Text failure handling

- If one label comes out misspelled or garbled, first try an edit with `--edit` that fixes only that label.
- If more than one label is wrong, regenerate with fewer labels.
- If it fails twice, fall back to no-text mode and tell the user.
