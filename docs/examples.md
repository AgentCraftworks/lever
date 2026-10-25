# Examples

Illustrative exchanges, abbreviated. The numbers are made up; the shapes are real. Each card is one command and roughly what comes back.

Invoke any skill as `/<skill> <your ask>`. If you don't know which one, use `/lever <your ask>`.

## Front door

![/lever](examples/lever.png)

## Loop: make an existing thing measurably better

![/find-the-loop](examples/find-the-loop.png)

![/experiment-arms](examples/experiment-arms.png)

## Build: something new, no signal yet

![/brief](examples/brief.png)

![/refactor-pipeline](examples/refactor-pipeline.png)

## Getting work landed

![/pr-shepherd](examples/pr-shepherd.png)

![/cross-model-review](examples/cross-model-review.png)

## Run: work that should happen without you

![/automate-it](examples/automate-it.png)

## You: get better at steering agents

![/prompt-mirror](examples/prompt-mirror.png)

![/steer-once](examples/steer-once.png)

---

The cards are rendered from [`examples/examples.html`](examples/examples.html). To change one, edit the HTML and run:

```bash
NODE_PATH=/path/to/node_modules node docs/examples/render.mjs   # needs playwright, @fontsource/mona-sans, @fontsource/monaspace-neon
```
