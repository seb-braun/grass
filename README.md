# grass

This repository is for demonstration purposes only. It is a playground for
experimenting with the GitHub CLI and trying out basic GitHub workflows.

It is not intended for production use.

## Demo app

Open [index.html](index.html) in your browser. No dependencies, installation, or
build step are required.

Click **Plant a seedling** to add a randomly chosen leafy plant, cactus, sunflower,
or succulent to your virtual garden. Each click makes a fresh random choice, so
the same plant can appear more than once. Click **Reset** to clear the garden and
counter. Both buttons also work with keyboard navigation.

Plant images are included in the repository, so the app works offline. Keep all
four SVG files (`plant.svg`, `cactus.svg`, `sunflower.svg`, and `succulent.svg`)
alongside `index.html`.

To serve the app locally instead, run this command from the repository directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.
