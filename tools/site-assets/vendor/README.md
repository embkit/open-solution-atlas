# Vendored third-party assets

These files are **vendored**, not fetched at build or run time. The published
site must keep working when a CDN is unreachable — for readers behind a
restricted network, a corporate proxy, or in a jurisdiction where
`cdn.jsdelivr.net` is throttled. Loading them from a CDN made the search box
and every diagram silently fail in exactly those conditions, which is the
opposite of what this catalog promises.

Each file's SHA-384 is pinned in `tools/build-site.py`
(`VENDOR_EXPECTED`). The build **fails** if a file is missing or does not
match its pin, so an accidental edit — or a poisoned upstream copy — cannot
ship silently. Bump the pin in the same commit that replaces the file.

| File | Upstream | Version | License | SHA-384 (base64, SRI) |
|---|---|---|---|---|
| `fuse.min.js` | [fuse.js](https://www.fusejs.io/) | 7.0.0 | Apache-2.0 | `PCSoOZTpbkikBEtd/+uV3WNdc676i9KUf01KOA8CnJotvlx8rRrETbDuwdjqTYvt` |
| `mermaid.min.js` | [mermaid](https://mermaid.js.org/) | 11.4.1 | MIT | `rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I` |

Both were retrieved from `https://cdn.jsdelivr.net/npm/<pkg>@<ver>/dist/<file>`
and verified with `sha384sum` before being committed.

## License obligations

- **fuse.js** — Apache License 2.0. The minified bundle keeps its license
  header; the full text is available at
  <https://www.apache.org/licenses/LICENSE-2.0>.
- **mermaid** — MIT. Copyright (c) 2014 - 2024 Knut Sveidqvist; the full text
  is available at <https://opensource.org/license/mit>.

Both licenses are compatible with this repository's dual license
(CC BY-SA 4.0 for content, MIT for code) because these files are
**third-party dependencies**, not contributed repository content.

## Updating a pinned file

```bash
# 1. fetch the new release
curl -sSL -o tools/site-assets/vendor/<file> \
  "https://cdn.jsdelivr.net/npm/<pkg>@<version>/dist/<file>"

# 2. recompute the SRI pin
python -c "import base64,hashlib,pathlib; \
  d=pathlib.Path('tools/site-assets/vendor/<file>').read_bytes(); \
  print('sha384-'+base64.b64encode(hashlib.sha384(d).digest()).decode())"

# 3. paste it into VENDOR_EXPECTED in tools/build-site.py
# 4. update the table above
```

Then run `python tools/build-site.py` — the integrity check passes only when
the code and this table agree.
