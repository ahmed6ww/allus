# QA Checklist

## Must pass

- It is 16:9 horizontal.
- The background is clean white.
- The character is present.
- The character performs the core action and is not just decoration.
- It does not copy an old example composition; it uses a fresh metaphor for the current article.
- The image is absurd, creative, and interesting.
- Clean and simple; the main subject takes no more than about 60% of the canvas.
- One image explains only one core structure.
- Labels match the count and length rules in language.md, are spelled correctly, and are readable.
- No text appears that was not in the label list, including the character's name.
- Orange is used only for the main path or arrows.
- Red is used only for key points, problems, warnings, or results.
- Blue is used only for secondary notes, feedback, or system state.

## Failure signals

If any of these appear, regenerate or do a local edit:

- A title in the top-left corner such as "Common Pitfalls / Workflow / System Architecture / Roadmap".
- The character looks like a mascot, a meme, or a cute cartoon.
- The image looks like a PPT, course slide, or formal flowchart.
- Too many elements, too many arrows, too many nodes.
- Text turns into long explanations.
- The background has paper texture, shadows, gradients, beige, or noise.
- Real UI screenshots or a techy interface look.
- Labels are badly misspelled or unreadable.
- The character's name or any unrequested text is written on the image.
- The image is too rigid and has no absurd metaphor.
- The composition is too similar to an old example in `assets/examples/`.

## How to iterate

- Too ordinary: make the character the subject of the action and add a strange but valid metaphor.
- Too complex: remove nodes, keep only one action and the labels allowed by language.md.
- Too cute: stress deadpan, blank serious expression, not cute, not a mascot.
- Too PPT: remove titles, borders, neat grids, and extra arrows; turn it into a hand-drawn scene.
- Too close to an old example: keep the core idea, replace the main object and the character's action.
- Wrong text: follow the text failure handling in references/language.md.

## Delivery test

A good image makes the reader first think "that's a bit strange", then understand the structure within one second.

If it first looks like a tutorial page instead of an absurd product sketch on white paper, it fails.
