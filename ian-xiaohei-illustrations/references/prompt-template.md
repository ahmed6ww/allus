# Image Prompt Template

Generate each image separately. Fill the variables from the article. Never combine several images into one.

## How to fill this

- `{LANGUAGE}` and `{LETTERING}` come from references/language.md: resolve the language first, then copy the lettering style from its table.
- The number of labels comes from the same table (for example 3 to 5 for English, 5 to 8 for Chinese). Drop the optional label slots you do not need.
- Labels are written in `{LANGUAGE}`. The rest of the prompt stays in English.
- If no-text mode is active, use the no-text variant below instead of the labels and lettering lines.

## Generation template

```text
Generate one standalone 16:9 horizontal article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten annotations in {LANGUAGE}. Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring character required:
A small solid-black absurd creature with white dot eyes, tiny thin legs, blank serious expression, slightly uneven hand-drawn body shape. The creature must perform the core conceptual action, not decorate the scene. Make it serious, deadpan, and slightly bizarre, not cute. Never write the character's name or any caption about the character on the image.

Theme:
{THEME}

Structure type (for composition only, never write it on the image):
{STRUCTURE: Workflow / System Slice / Before/After / Character States / Concept Metaphor / Layered Method / Map Route / Mini Comic Strip}

Core idea:
{CORE_IDEA}

Composition:
{COMPOSITION: where the creature is, what it is doing, the main objects, how information moves}

Suggested elements:
{element1} / {element2} / {element3} / {element4}

Handwritten labels ({LANGUAGE}): {label1} / {label2} / {label3} / {optional label4} / {optional label5}
Lettering style: {LETTERING}

Color use:
Black for main line art and the creature. Orange for the main flow, paths, and arrows. Red only for key warnings, problems, or results. Blue only for secondary notes, feedback, or system state.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use exactly the labels listed above and no other text. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## No-text variant

When no-text mode is active, replace the two lines starting with "Handwritten labels" and "Lettering style" with:

```text
No text, letters, numbers, or labels anywhere in the image. Communicate only through the drawing.
```

Also change "Sparse red/orange/blue handwritten annotations in {LANGUAGE}" in the Visual DNA to "Sparse red/orange/blue hand-drawn marks and arrows", and change "Use exactly the labels listed above and no other text" in the constraints to "No text of any kind".

## Image edit prompts

Remove a title in the top-left corner:

```text
Edit the provided image. Remove only the handwritten title "{TEXT_TO_REMOVE}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

Make the character more central:

```text
Regenerate this illustration with the same core meaning and simple layout, but make the black character more central to the conceptual action. The black character should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, and not cute.
```
