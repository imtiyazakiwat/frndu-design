# Frndu design

Clickable prototype and generated SVG UI frames for Frndu.

- Live: https://frndu-prototype.vercel.app
- `index.html`, `img/`, `vercel.json`: the Vercel site (static, no build step). `img/` holds the placeholder photos the frames load.
- `design/`: generator (`design/_gen/`), all SVG frames, references (`design/_refs/`), photo sources (`design/_assets/photos/`), `design/README.md` (screens + open questions) and `design/HANDOFF.md`.

Rebuild:

```sh
cd design/_gen
python3 build.py                              # frames + design/prototype/index.html
node flowcheck.js ../prototype/index.html     # must print "no errors"
cp ../prototype/index.html ../../index.html
```
