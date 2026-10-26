#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Privacy Policy generator for Google Play apps.

Usage:
    python3 generate.py

Reads apps.json + templates/ and writes static pages into docs/
(the directory GitHub Pages publishes from).

To add / remove / rename an app or change the contact email, edit apps.json
and re-run this script. No dependencies beyond the Python standard library.
"""

import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(ROOT, "apps.json")
TEMPLATE_POLICY = os.path.join(ROOT, "templates", "policy.html")
TEMPLATE_INDEX = os.path.join(ROOT, "templates", "index.html")
OUT_DIR = os.path.join(ROOT, "docs")

# ---------------------------------------------------------------------------
# Per-category content. Edit here to customise what each type of app declares.
# ---------------------------------------------------------------------------
CATEGORY_CONTENT = {
    "dashcam": {
        "permissions": [
            ("Camera", "to record driving video through your connected dash camera."),
            ("Microphone (optional)", "to record in-cabin or event audio, only if you enable it."),
            ("Location (optional)", "to attach GPS-based location tags to recordings, only if you enable it."),
            ("Storage", "to save recorded videos to your device&#8217;s local storage."),
            ("Background / ongoing operation (optional)",
             "to continue recording in the background if you turn on that feature."),
        ],
        "collected": [
            ("Video / camera content",
             "recorded when you use the recording feature. Recorded media is stored locally on your device by "
             "default and is not automatically uploaded to our servers."),
            ("Audio content (optional)",
             "collected only if you explicitly enable audio recording."),
            ("Location data (optional)",
             "collected only if you enable GPS tagging, and can be turned off at any time."),
            ("Stored files",
             "saved videos and settings you choose to keep on your device."),
        ],
    },
    "wifi_tool": {
        "permissions": [
            ("Camera", "to scan Wi-Fi QR codes."),
            ("Location", "to discover nearby Wi-Fi networks (required by the platform when scanning for networks)."),
            ("Storage", "to save or share QR-code images you generate."),
            ("Internet", "to load and display Wi-Fi connection details where needed."),
        ],
        "collected": [
            ("QR code content",
             "the Wi-Fi network information contained in QR codes that you actively scan or generate, "
             "processed locally on your device."),
            ("Nearby network information",
             "discovered under your location permission so you can connect to or generate a QR code for a network."),
            ("Camera frames",
             "used only to detect and decode QR codes."),
        ],
    },
}


def to_li(items, with_desc=True):
    """Render a list of (title, desc) tuples into <li> items."""
    rows = []
    for title, desc in items:
        if with_desc:
            rows.append("<li><strong>%s</strong> &#8212; %s</li>" % (title, desc))
        else:
            rows.append("<li>%s</li>" % title)
    return "\n    ".join(rows)


def render(template, tokens):
    out = template
    for key, value in tokens.items():
        out = out.replace("{{%s}}" % key, value)
    return out


def main():
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)

    company = cfg["company"]
    last_updated = company.get("last_updated") or date.today().isoformat()

    with open(TEMPLATE_POLICY, encoding="utf-8") as f:
        policy_tpl = f.read()
    with open(TEMPLATE_INDEX, encoding="utf-8") as f:
        index_tpl = f.read()

    cards = []
    for app in cfg["apps"]:
        cat = CATEGORY_CONTENT.get(app["category"], CATEGORY_CONTENT["dashcam"])
        perm_items = to_li(cat["permissions"], with_desc=True)
        collected_items = to_li(cat["collected"], with_desc=True)

        tokens = {
            "APP_NAME": app["name"],
            "COMPANY_NAME": company["legal_name"],
            "CONTACT_EMAIL": app.get("contact_email") or company["contact_email"],
            "LAST_UPDATED": last_updated,
            "SHORT_DESC": app.get("short_desc", "a mobile application"),
            "PERMISSIONS_DATA_LIST": collected_items,
            "PERMISSIONS_LIST": perm_items,
        }
        html = render(policy_tpl, tokens)

        app_dir = os.path.join(OUT_DIR, app["id"])
        os.makedirs(app_dir, exist_ok=True)
        with open(os.path.join(app_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        cards.append(
            '<a class="card" href="./%s/">\n'
            '  <h2>%s</h2>\n'
            '  <p>%s</p>\n'
            '</a>' % (app["id"], app["name"], app.get("short_desc", ""))
        )

    index_tokens = {
        "COMPANY_NAME": company["legal_name"],
        "CONTACT_EMAIL": company["contact_email"],
        "LAST_UPDATED": last_updated,
        "YEAR": str(date.today().year),
        "APP_CARDS": "\n  ".join(cards),
    }
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render(index_tpl, index_tokens))

    # Tell GitHub Pages not to run Jekyll over our static files.
    with open(os.path.join(OUT_DIR, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    print("Generated %d policy pages under %s" % (len(cfg["apps"]), OUT_DIR))
    for app in cfg["apps"]:
        print("  - docs/%s/index.html  (%s)" % (app["id"], app["name"]))


if __name__ == "__main__":
    main()
