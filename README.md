# privacy-policy

Privacy policies for the applications published by **Shenzhen Haotek Technology Co., Limited**.

Static, script-generated privacy policy pages intended to be served via **GitHub Pages** and referenced from
Google Play / app store listings.

## Applications

| App | Policy URL |
|-----|-----------|
| MobileCam | `docs/mobilecam/index.html` |
| CamBoss | `docs/camboss/index.html` |
| Wi-Fi QR | `docs/wifi-qr/index.html` |
| O-VisionRide | `docs/o-visionride/index.html` |
| AukeyDash | `docs/aukeydash/index.html` |
| PAPAGO!Link | `docs/papago-link/index.html` |

## Structure

```
apps.json               # company + per-app configuration (name, category, contact email)
templates/policy.html   # single English privacy-policy template
templates/index.html    # landing page listing all apps
generate.py             # generator (stdlib only, python3)
docs/                   # generated output, published by GitHub Pages
```

## Usage

Edit `apps.json` (add / remove / rename apps, change contact email, update date), then:

```bash
python3 generate.py
```

Generated pages are written to `docs/`. Per-category permission & data declarations live in
`CATEGORY_CONTENT` inside `generate.py` (currently `dashcam` and `wifi_tool`).

## Deploy on GitHub Pages

1. Push `main` to the remote:
   ```bash
   git add -A && git commit -m "Generate privacy policies" && git push origin main
   ```
2. In the repo **Settings → Pages**, under *Build and deployment*:
   - Source: **Deploy from a branch**
   - Branch: **main** → folder **/docs**
   - Save.

The site publishes at:
`https://shenzhen-haotek-technology-co-limited.github.io/privacy-policy/`

Per-app URLs, e.g. `https://shenzhen-haotek-technology-co-limited.github.io/privacy-policy/mobilecam/`.

Put the corresponding URL in each app's Play Console **Privacy Policy** field.

## License

See `LICENSE`.
