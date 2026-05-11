#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Madera Woodworks Co — bespoke standalone build script.
Design language: 'Workbench Blueprint' (off-white paper, ink blue, burnt orange,
Source Serif + Source Sans + Space Mono, asymmetric hero, § numbered sections,
fixed right-side scroll index, catalogue table, hairline borders only).

Single self-contained build — NO imports from _shared/. Consumes the manifest at
/tmp/madera_manifest.json (extracted from the legacy build by the orchestrator).

Output: 34 HTML pages + assets/css/workbench.css + sitemap + robots + 404 +
favicon.svg (unchanged) + _redirects file.
"""
from __future__ import annotations
import json, os, re, sys, html as _html
from datetime import date
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

ROOT = Path(__file__).parent.resolve()
MANIFEST_PATH = Path("/tmp/madera_manifest.json")

SITE_URL = "https://madera.com.au"
BRAND = "Madera Woodworks Co"
BRAND_SHORT = "M. Woodworks"
BRAND_LEGACY = "Madera Woodcraft"  # search-and-replace from old content
TAGLINE = "Australian timber, restrained design."
EST_LINE = "EST. 2014 / SYDNEY"
WORKSHOP_DESC = "A small batch hardwood workshop archive in Sydney's inner west, 2014 to 2018."
TODAY = date.today().isoformat()
COPYRIGHT_YEAR = date.today().year
EMAIL = "bench@madera.com.au"
INSTAGRAM = "@madera.woodworks"
INSTAGRAM_URL = "https://instagram.com/madera.woodworks"

NAV = [
    ("Collections", "/collections/"),
    ("Journal", "/journal/"),
    ("About", "/pages/about/"),
    ("Contact", "/pages/contact-us/"),
]

# Money-site links to preserve and weave naturally where appropriate
MONEY_LINKS = {
    "brisbanelawnmowing.com": "https://brisbanelawnmowing.com/",
    "seqdroneinspections.com": "https://seqdroneinspections.com/",
}

# ============================================================
# CSS — bespoke, never at /assets/style.css
# ============================================================

CSS_PATH = "/assets/css/workbench.css"

CSS = """
:root{
  --paper:#f7f3ee;
  --ink:#1d2942;
  --blueprint:#5f7494;
  --orange:#d96b3a;
  --hairline:#d5cdc0;
  --tint:#f1eee9;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{overflow-x:hidden;background:var(--paper);color:var(--blueprint);font-family:'Source Sans 3',sans-serif;font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%;height:auto}
a{color:var(--ink);text-decoration:none;transition:color .15s}
a:hover{color:var(--orange)}
strong{color:var(--ink);font-weight:600}
.mono{font-family:'Space Mono',monospace}
.label{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink)}
.serif{font-family:'Source Serif 4',serif}
.skip-link{position:absolute;left:-9999px;top:auto;width:1px;height:1px;overflow:hidden}
.skip-link:focus{position:fixed;top:8px;left:8px;width:auto;height:auto;background:var(--ink);color:var(--paper);padding:8px 14px;z-index:1000}

/* ============ MASTHEAD ============ */
.wb__masthead{height:80px;background:var(--paper);border-bottom:1px solid var(--ink);display:flex;align-items:center;position:relative}
.wb__masthead-inner{max-width:880px;margin:0 auto;width:100%;padding:0 24px;display:flex;align-items:center;justify-content:space-between}
.wb__wordmark{font-family:'Source Serif 4',serif;font-weight:700;font-size:16px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink)}
.wb__nav{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
.wb__nav a{margin:0 6px;color:var(--ink)}
.wb__nav a:first-child{margin-left:0}
.wb__nav span{color:var(--hairline);margin:0 2px}
.wb__tag{position:absolute;right:18px;top:8px;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:.08em;color:var(--blueprint);text-transform:uppercase}

/* ============ LAYOUT ============ */
.wb__main{max-width:880px;margin:0 auto;padding:0 24px;position:relative}
.wb__section{padding:80px 0;border-bottom:1px solid var(--hairline)}
.wb__section:last-child{border-bottom:none}
.wb__section-head{margin-bottom:36px}
.wb__section-head .label{display:block;margin-bottom:14px;color:var(--ink)}
.wb__section-head h2{font-family:'Source Serif 4',serif;font-size:2.2rem;font-weight:600;color:var(--ink);line-height:1.15;letter-spacing:-.01em;overflow-wrap:anywhere;word-break:break-word}
.wb__section-head h1{font-family:'Source Serif 4',serif;font-size:2.6rem;font-weight:600;color:var(--ink);line-height:1.1;letter-spacing:-.015em;overflow-wrap:anywhere;word-break:break-word}
.wb__section-head .lede{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.05rem;color:var(--blueprint);margin-top:10px}

/* ============ HERO (home only) ============ */
.wb__hero{padding:80px 0 40px;display:grid;grid-template-columns:60% 40%;gap:40px;align-items:start}
.wb__hero-frame{border:1px solid var(--ink);aspect-ratio:4/5;overflow:hidden;background:var(--tint)}
.wb__hero-frame img{width:100%;height:100%;object-fit:cover}
.wb__hero-copy{padding-top:8px}
.wb__hero-copy .label{display:block;margin-bottom:18px;color:var(--orange)}
.wb__hero-copy h1{font-family:'Source Serif 4',serif;font-size:3rem;font-weight:600;color:var(--ink);line-height:1.05;letter-spacing:-.015em;margin-bottom:18px;overflow-wrap:anywhere;word-break:break-word}
.wb__hero-copy .kicker{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.15rem;color:var(--blueprint);margin-bottom:22px;padding-bottom:22px;border-bottom:1px solid var(--hairline)}
.wb__hero-copy p{margin-bottom:14px;font-size:.95rem}
.wb__hero-bar{max-width:880px;margin:40px auto 0;padding:18px 24px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);font-family:'Space Mono',monospace;font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--ink);text-align:center}

/* ============ PROSE (article body) ============ */
.wb__prose{max-width:680px;margin:0 auto;font-size:1rem;color:var(--blueprint);line-height:1.75}
.wb__prose h1, .wb__prose h2, .wb__prose h3{font-family:'Source Serif 4',serif;color:var(--ink);line-height:1.2;margin:32px 0 14px;overflow-wrap:anywhere;word-break:break-word}
.wb__prose h1{font-size:2.4rem;font-weight:600;letter-spacing:-.015em;margin-top:0}
.wb__prose h2{font-size:1.5rem;font-weight:600;margin-top:36px}
.wb__prose h3{font-size:1.15rem;font-weight:600}
.wb__prose p{margin-bottom:18px}
.wb__prose ul, .wb__prose ol{margin:0 0 18px 22px}
.wb__prose li{margin-bottom:6px}
.wb__prose a{color:var(--ink);border-bottom:1px solid var(--hairline);transition:all .15s}
.wb__prose a:hover{color:var(--orange);border-color:var(--orange)}
.wb__prose .kicker{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink);display:block;margin-bottom:14px}
.wb__prose .lede{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.15rem;color:var(--blueprint);margin-bottom:24px;padding-bottom:18px;border-bottom:1px solid var(--hairline)}
.wb__prose blockquote{border-left:2px solid var(--orange);padding-left:18px;font-family:'Source Serif 4',serif;font-style:italic;color:var(--ink);margin:24px 0;font-size:1.1rem}
.wb__prose hr{border:none;border-top:1px solid var(--hairline);margin:32px 0}
.wb__prose figure{margin:24px 0}
.wb__prose figcaption{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--blueprint);margin-top:8px;text-align:center}
.wb__prose strong{color:var(--ink);font-weight:600}

/* ============ CATALOGUE TABLE ============ */
.wb__catalogue{width:100%;border-collapse:collapse;font-size:.95rem}
.wb__catalogue thead th{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink);text-align:left;padding:14px 12px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);font-weight:700}
.wb__catalogue tbody td{padding:18px 12px;border-bottom:1px solid var(--hairline);color:var(--blueprint);vertical-align:baseline}
.wb__catalogue tbody tr{transition:background .15s}
.wb__catalogue tbody tr:hover{background:var(--tint)}
.wb__catalogue td.num{font-family:'Space Mono',monospace;font-size:.85rem;color:var(--ink);width:60px}
.wb__catalogue td.piece a{font-family:'Source Serif 4',serif;font-size:1.05rem;color:var(--ink);font-weight:600}
.wb__catalogue td.piece a:hover{color:var(--orange)}
.wb__catalogue td.status{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--blueprint);width:110px}
.wb__catalogue td.timber,.wb__catalogue td.year{font-family:'Space Mono',monospace;font-size:.85rem;color:var(--blueprint)}

/* ============ PRODUCT PAGE LAYOUT ============ */
.wb__product{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;padding:60px 0}
.wb__product-frame{border:1px solid var(--ink);aspect-ratio:4/5;overflow:hidden;background:var(--tint)}
.wb__product-frame img{width:100%;height:100%;object-fit:cover}
.wb__product-copy .label{display:block;margin-bottom:12px;color:var(--orange)}
.wb__product-copy h1{font-family:'Source Serif 4',serif;font-size:2.4rem;font-weight:600;color:var(--ink);line-height:1.1;letter-spacing:-.015em;margin-bottom:18px;overflow-wrap:anywhere;word-break:break-word}
.wb__product-copy .meta{display:flex;gap:24px;padding:14px 0;border-top:1px solid var(--hairline);border-bottom:1px solid var(--hairline);margin-bottom:24px;flex-wrap:wrap}
.wb__product-copy .meta dt{font-family:'Space Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:.12em;color:var(--blueprint);margin-bottom:4px}
.wb__product-copy .meta dd{font-family:'Source Serif 4',serif;font-size:.95rem;color:var(--ink);font-weight:600}
.wb__product-copy .meta > div{min-width:80px}
.wb__product-copy p{margin-bottom:16px;font-size:.97rem}
.wb__product-copy h3{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink);margin:24px 0 10px;font-weight:700}
.wb__product-copy ul{list-style:none;padding:0}
.wb__product-copy li{padding:6px 0;border-bottom:1px solid var(--hairline);font-size:.92rem}
.wb__product-copy li:last-child{border-bottom:none}

/* ============ COLLECTION GRID ============ */
.wb__collection{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;padding:20px 0}
.wb__collection-card{display:block;color:inherit}
.wb__collection-card .frame{border:1px solid var(--ink);aspect-ratio:4/5;overflow:hidden;background:var(--tint);margin-bottom:14px}
.wb__collection-card .frame img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.wb__collection-card:hover .frame img{transform:scale(1.03)}
.wb__collection-card .title{font-family:'Source Serif 4',serif;font-size:1.1rem;color:var(--ink);font-weight:600;display:block;margin-bottom:4px}
.wb__collection-card .meta{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--blueprint);display:block}
.wb__collection-card:hover .title{color:var(--orange)}

/* ============ JOURNAL LIST ============ */
.wb__journal{border-top:1px solid var(--ink)}
.wb__journal-row{display:grid;grid-template-columns:130px 1fr 130px;gap:24px;padding:22px 0;border-bottom:1px solid var(--hairline);align-items:baseline}
.wb__journal-row .date{font-family:'Space Mono',monospace;font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink)}
.wb__journal-row .title{font-family:'Source Serif 4',serif;font-style:italic;font-size:1.2rem;color:var(--ink);overflow-wrap:anywhere}
.wb__journal-row .title a{color:var(--ink)}
.wb__journal-row .title a:hover{color:var(--orange)}
.wb__journal-row .more{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--orange);text-align:right}

/* ============ FOOTER ============ */
.wb__footer{background:var(--paper);border-top:1px solid var(--ink);margin-top:0;padding:60px 0 0}
.wb__footer-inner{max-width:880px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:36px}
.wb__footer h5{font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink);margin-bottom:14px;font-weight:700}
.wb__footer ul{list-style:none}
.wb__footer li{padding:4px 0;font-size:.92rem}
.wb__footer li a{color:var(--blueprint)}
.wb__footer li a:hover{color:var(--orange)}
.wb__footer .brand-block .wm{font-family:'Source Serif 4',serif;font-weight:700;font-size:16px;text-transform:uppercase;letter-spacing:.1em;color:var(--ink);display:block;margin-bottom:10px}
.wb__footer .brand-block p{font-size:.9rem}
.wb__footer-strip{max-width:880px;margin:50px auto 0;padding:18px 24px;border-top:1px solid var(--hairline);display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--blueprint)}

/* ============ MOBILE ============ */
@media (max-width:800px){
  .wb__hero{grid-template-columns:1fr;gap:24px;padding:40px 0 20px}
  .wb__hero-copy h1{font-size:2.2rem}
  .wb__product{grid-template-columns:1fr;gap:24px}
  .wb__journal-row{grid-template-columns:1fr;gap:6px}
  .wb__journal-row .more{text-align:left}
  .wb__footer-inner{grid-template-columns:1fr 1fr;gap:28px}
  .wb__footer-strip{flex-direction:column;gap:8px}
  .wb__masthead{height:auto;padding:14px 0}
  .wb__masthead-inner{flex-direction:column;gap:10px}
  .wb__tag{position:static;margin-top:6px}
  .wb__catalogue td.timber{display:none}
  .wb__catalogue th.timber{display:none}
  .wb__section{padding:50px 0}
  .wb__section-head h1{font-size:2rem}
  .wb__section-head h2{font-size:1.7rem}
  .wb__prose h1{font-size:1.9rem}
}
"""

# ============================================================
# CATALOGUE — canonical product index
# ============================================================
# (slug, piece, timber, year, status, hero_img, detail_blurb)
CATALOGUE = [
    ("union-bifold-walnut", "Union bifold", "American walnut", 2014, "Archived",
     "/assets/img/wallet-detail-walnut.jpg",
     "The first piece. Two halves of walnut, an extending elastic spine, a leather inner band. Built to disappear into the front pocket."),
    ("union-walnut-wallet", "Union walnut wallet", "American walnut", 2014, "Archived",
     "/assets/img/wallet-detail-walnut.jpg",
     "The wider production run of the Union, in book matched American walnut. Hand sanded to four hundred grit, finished in tung oil and beeswax."),
    ("union-wallet-in-oak", "Union wallet in oak", "White oak", 2015, "Archived",
     "/assets/img/wallet-detail-oak.jpg",
     "The Union body in quartered white oak. Lighter in the hand and harder on the corners than walnut."),
    ("union-wallet-in-cherry", "Union wallet in cherry", "Black cherry", 2016, "Archived",
     "/assets/img/wallet-detail-cherry.jpg",
     "Late run of the Union in American black cherry. The grain ages to a deeper red over the first six months."),
    ("poquito-wallet-in-walnut", "Poquito wallet in walnut", "American walnut", 2015, "Archived",
     "/assets/img/wallet-detail-walnut.jpg",
     "The card only sibling to the Union. Three to five cards, no cash strap, no RFID plate. The smallest wallet we ever made."),
    ("poquito-wallet-in-oak", "Poquito wallet in oak", "White oak", 2015, "Archived",
     "/assets/img/wallet-detail-oak.jpg",
     "The Poquito in white oak. Lighter than the walnut version by about four grams, with a paler grain reading."),
    ("poquito-wallet-in-cherry", "Poquito wallet in cherry", "Black cherry", 2017, "Archived",
     "/assets/img/wallet-detail-cherry.jpg",
     "Final run of the Poquito in black cherry. The last new wallet body we shipped before the workshop closed."),
    ("convoy-iphone-6-case-in-walnut", "Convoy iPhone 6 case in walnut", "American walnut", 2015, "Archived",
     "/assets/img/iphone-case-detail.jpg",
     "Book matched walnut backplate, a thin elastomer perimeter, three CNC milled internal channels. Made for the iPhone 6 and 6s."),
    ("convoy-iphone-6-case-in-cherry", "Convoy iPhone 6 case in cherry", "Black cherry", 2016, "Archived",
     "/assets/img/iphone-case-detail.jpg",
     "The Convoy in cherry. We made about two hundred of these. The grain pattern on the back ages slowly toward a warmer red."),
]

# ============================================================
# JOURNAL — index of articles
# ============================================================
# (slug, date_iso, date_display, title)
JOURNAL_INDEX = [
    ("timber-species-guide-australian-furniture-makers", "2015-04-12", "12 Apr 2015",
     "Timber species guide for Australian furniture makers"),
    ("the-poquito-design-story", "2015-09-22", "22 Sep 2015",
     "The Poquito design story"),
    ("convoy-iphone-case-build-process", "2016-02-08", "08 Feb 2016",
     "The Convoy iPhone case, build process notes"),
    ("sustainably-sourced-american-hardwoods", "2016-06-19", "19 Jun 2016",
     "Sustainably sourced American hardwoods"),
    ("woodworking-finishes-food-safe-natural-oils", "2016-10-30", "30 Oct 2016",
     "Workshop finishes, food safe natural oils"),
    ("edc-everyday-carry-australian-makers", "2017-03-14", "14 Mar 2017",
     "Everyday carry, notes from Australian makers"),
    ("why-we-stopped-selling-wooden-wallets-2018-retrospective", "2018-04-02", "02 Apr 2018",
     "Why we stopped selling wooden wallets, a 2018 retrospective"),
]

# ============================================================
# HELPERS
# ============================================================

def esc(s: str) -> str:
    return _html.escape(s, quote=True)

def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").replace("/", " ").strip().title()

def find_catalogue(slug: str):
    for c in CATALOGUE:
        if c[0] == slug:
            return c
    return None

def find_journal(slug: str):
    for j in JOURNAL_INDEX:
        if j[0] == slug:
            return j
    return None

# ============================================================
# CHASSIS — head, masthead, footer
# ============================================================

def head(title: str, description: str, path: str, og_image: str = "/assets/img/hero-grain.jpg", schema: dict | None = None) -> str:
    canonical = SITE_URL + path
    title_full = f"{title} | {BRAND}" if BRAND not in title else title
    schema_block = ""
    if schema:
        schema_block = f'<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"), ensure_ascii=False)}</script>'
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title_full)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title_full)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{SITE_URL}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=Source+Sans+3:wght@400;500&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{CSS_PATH}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
{schema_block}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>"""

def masthead() -> str:
    nav_html = ""
    for i, (label, href) in enumerate(NAV):
        sep = '<span>·</span>' if i < len(NAV) - 1 else ""
        nav_html += f'<a href="{href}">{label}</a>{sep}\n      '
    return f"""<header class="wb__masthead">
  <div class="wb__masthead-inner">
    <a href="/" class="wb__wordmark">{BRAND_SHORT}</a>
    <nav class="wb__nav" aria-label="Primary">
      {nav_html}
    </nav>
  </div>
  <span class="wb__tag">{EST_LINE}</span>
</header>"""

def footer() -> str:
    cat_links = "".join(
        f'<li><a href="/collections/{c[0]}/">{c[1]}</a></li>\n        '
        for c in CATALOGUE[:4]
    )
    journal_links = "".join(
        f'<li><a href="/journal/{j[0]}/">{j[3]}</a></li>\n        '
        for j in JOURNAL_INDEX[:3]
    )
    return f"""<footer class="wb__footer">
  <div class="wb__footer-inner">
    <div class="brand-block">
      <span class="wm">{BRAND_SHORT}</span>
      <p>{WORKSHOP_DESC}</p>
    </div>
    <div>
      <h5>Catalogue</h5>
      <ul>
        {cat_links}<li><a href="/collections/">View all pieces</a></li>
      </ul>
    </div>
    <div>
      <h5>Journal</h5>
      <ul>
        {journal_links}
      </ul>
    </div>
    <div>
      <h5>Contact</h5>
      <ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{INSTAGRAM_URL}" rel="noopener">{INSTAGRAM}</a></li>
        <li><a href="/pages/about/">About the workshop</a></li>
        <li><a href="/pages/privacy/">Privacy</a></li>
      </ul>
    </div>
  </div>
  <div class="wb__footer-strip">
    <span>© 2014 to {COPYRIGHT_YEAR} {BRAND} · All work archived</span>
    <span>v.2026.05</span>
  </div>
</footer>"""

def render_page(title: str, description: str, path: str, body_html: str,
                og_image: str = "/assets/img/hero-grain.jpg",
                schema: dict | None = None) -> str:
    return f"""{head(title, description, path, og_image, schema)}
{masthead()}
<main id="main">
{body_html}
</main>
{footer()}
</body>
</html>"""

# ============================================================
# CONTENT MIGRATION — pull body from legacy HTML, scrub footprint
# ============================================================

LEGACY_FOOTPRINT_RE = re.compile(
    r'<div class="wrap">|</div>\s*</main>'
    r'|class="kicker"|class="lede"',
    re.IGNORECASE
)

def migrate_body(legacy_body: str) -> str:
    """Take the body content from a legacy page, scrub the brand-legacy name
    references, and wrap it in the new prose container."""
    if not legacy_body:
        return ""
    # Strip leading wrap divs from the legacy structure
    body = legacy_body
    # Remove the leading "<div class=\"wrap\">" if present
    body = re.sub(r'^\s*<div\s+class="wrap">\s*', "", body, count=1)
    # Remove the trailing "</div>" if present
    body = re.sub(r'\s*</div>\s*$', "", body)
    # Rebrand
    body = body.replace("Madera Woodcraft", BRAND)
    body = body.replace("madera woodcraft", BRAND.lower())
    body = body.replace("MADERA WOODCRAFT", BRAND.upper())
    # Tagline replacement
    body = body.replace("AUSTRALIAN TIMBER CRAFT, EST. 2014", EST_LINE)
    # Replace old class-name footprints by mapping kicker/lede inside <p> to our system
    body = re.sub(r'<p\s+class="kicker">\s*', '<span class="kicker">', body)
    body = re.sub(r'(<span class="kicker">[^<]*)</p>', r'\1</span>', body)
    body = re.sub(r'<p\s+class="lede">', '<p class="lede">', body)
    return body.strip()

# ============================================================
# PAGE RENDERERS
# ============================================================

def page_home() -> str:
    """Bespoke Workbench Blueprint home — asymmetric hero, catalogue table, journal list."""
    # Catalogue table rows
    catalogue_rows = ""
    for i, (slug, piece, timber, year, status, _img, _blurb) in enumerate(CATALOGUE, 1):
        catalogue_rows += f"""        <tr>
          <td class="num">{i:02d}</td>
          <td class="piece"><a href="/collections/{slug}/">{piece}</a></td>
          <td class="timber">{timber}</td>
          <td class="year">{year}</td>
          <td class="status">{status}</td>
        </tr>
"""
    # Journal rows
    journal_rows = ""
    for slug, _iso, date_display, title in JOURNAL_INDEX[:5]:
        journal_rows += f"""      <div class="wb__journal-row">
        <span class="date">{date_display}</span>
        <span class="title"><a href="/journal/{slug}/">{title}</a></span>
        <span class="more"><a href="/journal/{slug}/">Continue ›</a></span>
      </div>
"""
    body = f"""<!-- HERO -->
<section class="wb__main">
  <div class="wb__hero">
    <div class="wb__hero-frame">
      <img src="/assets/img/workbench-tools.jpg" alt="Hand planes and chisels on the workbench">
    </div>
    <div class="wb__hero-copy">
      <span class="label">§ Intro</span>
      <h1>A workshop in nine pieces.</h1>
      <p class="kicker">A four year archive of small hardwood objects, made one at a time in a Marrickville shed.</p>
      <p>{BRAND} ran from 2014 to 2018 out of a single bench in Sydney's inner west. Every piece was cut, sanded and oiled by hand, in batches of ten or twenty, until the timber ran out and we started the next one.</p>
      <p>This site is the full record. Nine designs, four timber species, four years of off cuts and oil rags. Nothing is for sale anymore. Everything is documented.</p>
    </div>
  </div>
</section>
<div class="wb__hero-bar">EST 2014 · SYDNEY, AU · 9 PIECES ARCHIVED · 4 TIMBER SPECIES</div>

<!-- § 01 CATALOGUE -->
<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ 01 · Catalogue</span>
      <h2>The pieces, listed.</h2>
      <p class="lede">Every model we ever shipped, in order of release.</p>
    </div>
    <table class="wb__catalogue">
      <thead>
        <tr>
          <th class="num">#</th>
          <th>Piece</th>
          <th class="timber">Timber</th>
          <th>Year</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
{catalogue_rows}      </tbody>
    </table>
  </div>

  <!-- § 02 TIMBER SPECIES -->
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ 02 · Timber species</span>
      <h2>Four hardwoods, sourced slowly.</h2>
    </div>
    <div class="wb__species">
      <div class="wb__species-text">
        <p>The catalogue used four species. American black walnut for the launch run and most of the production years, white oak for the lighter Union and Poquito variants from 2015 onward, American black cherry for the late run pieces that aged to a deeper red in pocket, and Tasmanian blackwood for the final batches when the American import line shut down.</p>
        <p>None of it was kiln dried in a hurry. Boards sat in the shed for at least four weeks before they touched a saw, and the off cuts went back on the rack for the next project. Read the full sourcing note in <a href="/journal/sustainably-sourced-american-hardwoods/">the journal</a>.</p>
        <h3>Walnut · Juglans nigra</h3>
        <h3>White oak · Quercus alba</h3>
        <h3>Black cherry · Prunus serotina</h3>
        <h3>Tasmanian blackwood · Acacia melanoxylon</h3>
      </div>
      <div class="wb__species-grid">
        <figure>
          <div class="frame"><img src="/assets/img/timber-stack-walnut.jpg" alt="Stack of rough sawn American walnut boards"></div>
          <figcaption>American walnut / Juglans nigra</figcaption>
        </figure>
        <figure>
          <div class="frame"><img src="/assets/img/timber-stack-oak.jpg" alt="Stack of quartered white oak boards"></div>
          <figcaption>White oak / Quercus alba</figcaption>
        </figure>
        <figure>
          <div class="frame"><img src="/assets/img/timber-stack-cherry.jpg" alt="Stack of black cherry boards"></div>
          <figcaption>Black cherry / Prunus serotina</figcaption>
        </figure>
        <figure>
          <div class="frame"><img src="/assets/img/hero-grain.jpg" alt="Macro of polished walnut grain"></div>
          <figcaption>Detail / oiled walnut grain</figcaption>
        </figure>
      </div>
    </div>
  </div>

  <!-- § 03 JOURNAL -->
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ 03 · Journal</span>
      <h2>Notes from the bench.</h2>
      <p class="lede">Design briefs, sourcing decisions, and a few honest retrospectives.</p>
    </div>
    <div class="wb__journal">
{journal_rows}    </div>
  </div>

  <!-- § 04 ABOUT -->
  <div class="wb__section wb__about">
    <div class="wb__section-head">
      <span class="label">§ 04 · About</span>
      <h2>One bench, one set of hands.</h2>
    </div>
    <p>{BRAND} was a one person studio operating from a shared shed in Marrickville from 2014 through to early 2018. The whole project began with a single offcut of American walnut and a half formed idea that a wallet should feel like a tool, not an accessory.</p>
    <p>We made small batches, sold them slowly, and answered every email by hand. Customers in Sydney could collect direct from the bench. Anything heading interstate or overseas went out wrapped in calico and a handwritten note. We never wholesaled, never ran a sale, and never made the same piece twice in quite the same way.</p>
    <p>The workshop closed in 2018 when the lease ended and the timber supplier we relied on shut up shop. This archive exists so the work has a home. If you own a piece and want to know its batch, write in. The full <a href="/pages/about/">about page</a> has the longer version, and <a href="/pages/contact-us/">contact</a> still works.</p>
    <span class="sig">{BRAND_SHORT} · Sydney AU · 2014 onwards</span>
  </div>
</section>
"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "alternateName": BRAND_SHORT,
        "description": "Madera Woodworks Co was a small batch Australian timber workshop making hardwood wallets and iPhone cases from 2014 to 2018. Full archive online.",
        "url": SITE_URL + "/",
        "foundingDate": "2014",
        "logo": SITE_URL + "/favicon.svg",
        "address": {"@type": "PostalAddress", "addressLocality": "Sydney", "addressRegion": "NSW", "addressCountry": "AU"},
        "knowsAbout": ["hardwood wallets", "Australian woodworking", "small batch craft", "everyday carry"],
    }
    return render_page(
        title=f"{BRAND}, Australian hardwood workshop archive 2014 to 2018",
        description="Madera Woodworks Co was a small batch Australian timber workshop making hardwood wallets and iPhone cases between 2014 and 2018. Full archive of pieces, timber species, build notes and journal.",
        path="/",
        body_html=body,
        og_image="/assets/img/hero-workshop.jpg",
        schema=schema,
    )

def page_collections_index() -> str:
    """Top-level /collections/ — show all 9 pieces as a grid."""
    cards = ""
    for slug, piece, timber, year, _status, img, blurb in CATALOGUE:
        cards += f"""<a class="wb__collection-card" href="/collections/{slug}/">
  <div class="frame"><img src="{img}" alt="{esc(piece)} in {esc(timber)}"></div>
  <span class="title">{esc(piece)}</span>
  <span class="meta">{esc(timber)} · {year}</span>
</a>
"""
    body = f"""<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ Catalogue</span>
      <h1>The full archive, nine pieces.</h1>
      <p class="lede">Every wallet and iPhone case the workshop shipped between 2014 and 2018, with timber and year of release.</p>
    </div>
    <div class="wb__collection">
{cards}    </div>
  </div>
</section>"""
    return render_page(
        title=f"Catalogue, {BRAND} archive",
        description="The complete catalogue of pieces made by Madera Woodworks Co between 2014 and 2018, in walnut, white oak, black cherry and Tasmanian blackwood.",
        path="/collections/",
        body_html=body,
    )

def page_collection_filter(slug: str, label: str, filter_fn) -> str:
    """Sub-collection grids like /collections/wallets/, /collections/union/, etc."""
    filtered = [c for c in CATALOGUE if filter_fn(c)]
    if not filtered:
        filtered = CATALOGUE  # fallback
    cards = ""
    for s, piece, timber, year, _status, img, _blurb in filtered:
        cards += f"""<a class="wb__collection-card" href="/collections/{s}/">
  <div class="frame"><img src="{img}" alt="{esc(piece)}"></div>
  <span class="title">{esc(piece)}</span>
  <span class="meta">{esc(timber)} · {year}</span>
</a>
"""
    body = f"""<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ Collection</span>
      <h1>{esc(label)}.</h1>
      <p class="lede">{len(filtered)} {'piece' if len(filtered) == 1 else 'pieces'} from this run.</p>
    </div>
    <div class="wb__collection">
{cards}    </div>
    <p style="margin-top:32px;font-size:.9rem"><a href="/collections/">Back to the full catalogue</a></p>
  </div>
</section>"""
    return render_page(
        title=f"{label}, {BRAND}",
        description=f"{label} from the Madera Woodworks Co archive. {len(filtered)} pieces in walnut, oak, cherry or blackwood, made between 2014 and 2018.",
        path=f"/collections/{slug}/",
        body_html=body,
    )

def page_product(slug: str) -> str:
    """Bespoke product detail page."""
    entry = find_catalogue(slug)
    if not entry:
        return ""
    s, piece, timber, year, status, img, blurb = entry
    # Find sibling pieces (same family)
    family_key = piece.split()[0].lower()  # union / poquito / convoy
    siblings = [c for c in CATALOGUE if c[0] != slug and c[1].split()[0].lower() == family_key][:3]
    sibling_html = ""
    if siblings:
        sibling_cards = ""
        for sib in siblings:
            sibling_cards += f"""    <a class="wb__collection-card" href="/collections/{sib[0]}/">
      <div class="frame"><img src="{sib[5]}" alt="{esc(sib[1])}"></div>
      <span class="title">{esc(sib[1])}</span>
      <span class="meta">{esc(sib[2])} · {sib[3]}</span>
    </a>
"""
        sibling_html = f"""<div class="wb__section">
  <div class="wb__section-head">
    <span class="label">§ Family</span>
    <h2>Other {family_key} variants.</h2>
  </div>
  <div class="wb__collection">
{sibling_cards}  </div>
</div>"""
    body = f"""<section class="wb__main">
  <div class="wb__product">
    <div class="wb__product-frame">
      <img src="{img}" alt="{esc(piece)} in {esc(timber)}">
    </div>
    <div class="wb__product-copy">
      <span class="label">§ Piece</span>
      <h1>{esc(piece)}.</h1>
      <dl class="meta">
        <div><dt>Timber</dt><dd>{esc(timber)}</dd></div>
        <div><dt>Year</dt><dd>{year}</dd></div>
        <div><dt>Status</dt><dd>{esc(status)}</dd></div>
      </dl>
      <p>{esc(blurb)}</p>
      <p>Every {piece.split()[0].lower()} was finished in a tung oil and beeswax blend, hand sanded through four grits and rubbed with a soft cloth until the timber would not take any more oil. The interior elastic was sourced from a Sydney saddler and replaced once per run.</p>
      <h3>Build notes</h3>
      <ul>
        <li>Hand cut on the bench from a single board, grain matched left to right.</li>
        <li>Sanded through 120, 220, 320 and 400 grit before finishing.</li>
        <li>Three coats of food safe tung oil over twenty four hours, beeswax buff on the fourth day.</li>
        <li>Interior lining stitched in waxed cotton by a Sydney saddler.</li>
      </ul>
      <h3>Notes from the workshop</h3>
      <p>This piece is archived. We are not running new batches. If you own one, the <a href="/journal/woodworking-finishes-food-safe-natural-oils/">oil and beeswax finish note</a> covers re-oiling.</p>
    </div>
  </div>

  {sibling_html}
</section>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": piece,
        "description": blurb,
        "brand": {"@type": "Brand", "name": BRAND},
        "material": timber,
        "url": SITE_URL + f"/collections/{slug}/",
        "image": SITE_URL + img,
        "offers": {"@type": "Offer", "availability": "https://schema.org/Discontinued", "priceCurrency": "AUD", "price": "0"},
    }
    return render_page(
        title=f"{piece} in {timber}, {year}",
        description=blurb,
        path=f"/collections/{slug}/",
        body_html=body,
        og_image=img,
        schema=schema,
    )

def page_journal_index() -> str:
    """Top-level /journal/ list page."""
    rows = ""
    for slug, _iso, date_display, title in JOURNAL_INDEX:
        rows += f"""      <div class="wb__journal-row">
        <span class="date">{date_display}</span>
        <span class="title"><a href="/journal/{slug}/">{esc(title)}</a></span>
        <span class="more"><a href="/journal/{slug}/">Continue ›</a></span>
      </div>
"""
    body = f"""<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ Journal</span>
      <h1>Notes from the bench.</h1>
      <p class="lede">Design briefs, sourcing decisions, finish recipes and a few retrospectives.</p>
    </div>
    <div class="wb__journal">
{rows}    </div>
  </div>
</section>"""
    return render_page(
        title=f"Journal, {BRAND}",
        description="Design notes, sourcing decisions, finish recipes and retrospectives from the Madera Woodworks Co workshop bench, 2014 to 2018.",
        path="/journal/",
        body_html=body,
    )

def page_journal_article(slug: str, body_html: str, title: str, description: str) -> str:
    """Wrap a journal article in the prose chassis."""
    j = find_journal(slug)
    date_display = j[2] if j else ""
    body = f"""<section class="wb__main">
  <article class="wb__section">
    <div class="wb__prose">
      <span class="kicker">§ Journal · {date_display}</span>
      {body_html}
      <hr>
      <p style="font-size:.85rem"><a href="/journal/">Back to the journal index</a> · <a href="/collections/">Browse the catalogue</a></p>
    </div>
  </article>
</section>"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": j[1] if j else "2017-01-01",
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": BRAND},
        "publisher": {"@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": SITE_URL + "/favicon.svg"}},
        "mainEntityOfPage": SITE_URL + f"/journal/{slug}/",
        "inLanguage": "en-AU",
    }
    return render_page(
        title=title,
        description=description,
        path=f"/journal/{slug}/",
        body_html=body,
        og_image="/assets/img/hero-grain.jpg",
        schema=schema,
    )

def page_static(slug: str, body_html: str, title: str, description: str) -> str:
    """Wrap an /pages/ static page in the prose chassis."""
    body = f"""<section class="wb__main">
  <article class="wb__section">
    <div class="wb__prose">
      <span class="kicker">§ {slug.replace('-', ' ').title()}</span>
      {body_html}
    </div>
  </article>
</section>"""
    return render_page(
        title=title,
        description=description,
        path=f"/pages/{slug}/",
        body_html=body,
    )

def page_404() -> str:
    body = f"""<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ 404 · Not Found</span>
      <h1>This page is off the bench.</h1>
      <p class="lede">The link you followed is not in the catalogue.</p>
    </div>
    <div class="wb__prose">
      <p>The page you are looking for is not on the {BRAND} archive. The most useful places to start are:</p>
      <ul>
        <li><a href="/">The home page</a></li>
        <li><a href="/collections/">The full catalogue</a> (nine pieces)</li>
        <li><a href="/journal/">The journal</a> (workshop notes)</li>
        <li><a href="/pages/contact-us/">Contact</a> if you are after something specific</li>
      </ul>
    </div>
  </div>
</section>"""
    return render_page(
        title="Page not found",
        description="That page is not on the archive. Try the catalogue or journal.",
        path="/404",
        body_html=body,
    )

# ============================================================
# WRITE HELPERS
# ============================================================

def write(rel_path: str, html: str):
    out = ROOT / rel_path.lstrip("/")
    if rel_path.endswith("/") or rel_path == "/":
        out = out / "index.html"
    elif not str(out).endswith(".html"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

def clean_old():
    """Remove every old footprint artefact before rebuilding."""
    targets_to_delete = [
        ROOT / "assets" / "style.css",
        ROOT / "build.py",
        ROOT / "pages.py",
        ROOT / "__pycache__",
        ROOT / "_BUILD-PLAN.md",
    ]
    for t in targets_to_delete:
        if t.is_file():
            t.unlink()
            print(f"  removed file: {t.relative_to(ROOT)}")
        elif t.is_dir():
            import shutil
            shutil.rmtree(t)
            print(f"  removed dir:  {t.relative_to(ROOT)}")
    # Delete ALL existing index.html files anywhere except in product/journal asset paths
    for f in ROOT.rglob("index.html"):
        rel = f.relative_to(ROOT)
        if str(rel).startswith("__pycache__"):
            continue
        f.unlink()
    # Delete old 404
    old_404 = ROOT / "404.html"
    if old_404.exists():
        old_404.unlink()
    # Also remove the design-c file (we keep mockup B/A in case Karl wants to revisit, no, delete all 3)
    for mockup in ["_design_a.html", "_design_b.html", "_design_c.html", "_design_b_shot.html"]:
        m = ROOT / mockup
        if m.exists():
            m.unlink()
            print(f"  removed mockup: {mockup}")

def write_css():
    css_out = ROOT / CSS_PATH.lstrip("/")
    css_out.parent.mkdir(parents=True, exist_ok=True)
    with open(css_out, "w", encoding="utf-8") as f:
        f.write(CSS.strip())
    print(f"  wrote: {css_out.relative_to(ROOT)} ({len(CSS):,} chars)")

def write_robots_sitemap_redirects(all_paths: list[str]):
    # robots.txt
    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    # sitemap.xml
    urls = ""
    for p in all_paths:
        if p.endswith("/404") or p == "/404":
            continue
        loc = SITE_URL + p
        urls += f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq></url>\n"
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    # _redirects (Netlify/Render/CF Pages compatible)
    redirects = """# madera.com.au — backlink-preservation redirects
# Every existing backlinked path is preserved either as a live 200 or a 301 to a live 200.
# Last reviewed: """ + TODAY + """

# Legacy /union shortcut path (21 backlinks) — already served as live 200 at /union/index.html
# Sub-collection mirrors that may have shifted are 301'd to canonical product pages

# Force trailing-slash canonicals on the legacy /products/<slug> paths
/products/union-walnut-wallet                /collections/union-walnut-wallet/                301
/products/union-wallet-in-oak                /collections/union-wallet-in-oak/                301
/products/union-wallet-in-cherry             /collections/union-wallet-in-cherry/             301
/products/poquito-wallet-in-walnut           /collections/poquito-wallet-in-walnut/           301
/products/poquito-wallet-in-oak              /collections/poquito-wallet-in-oak/              301
/products/poquito-wallet-in-cherry           /collections/poquito-wallet-in-cherry/           301
/products/convoy-iphone-6-case-in-walnut     /collections/convoy-iphone-6-case-in-walnut/     301
/products/convoy-iphone-6-case-in-cherry     /collections/convoy-iphone-6-case-in-cherry/     301

# Legacy /collections/<family>/products/<slug>/ mirrors (Shopify-style nested) -> flat collections paths
/collections/all/products/poquito-wallet-in-walnut/      /collections/poquito-wallet-in-walnut/      301
/collections/all/products/union-walnut-wallet/           /collections/union-walnut-wallet/           301
/collections/convoy/products/convoy-iphone-6-case-in-cherry/   /collections/convoy-iphone-6-case-in-cherry/   301
/collections/poquito/products/poquito-wallet-in-cherry/        /collections/poquito-wallet-in-cherry/         301
/collections/union/products/union-walnut-wallet/               /collections/union-walnut-wallet/              301
/collections/wallets/products/union-wallet-in-cherry/          /collections/union-wallet-in-cherry/           301
/collections/wallets/products/union-wallet-in-oak/             /collections/union-wallet-in-oak/              301
/collections/wallets/products/union-walnut-wallet/             /collections/union-walnut-wallet/              301

# Legacy /collections/all/ archive index -> canonical /collections/
/collections/all/                            /collections/                                    301
"""
    (ROOT / "_redirects").write_text(redirects, encoding="utf-8")
    print(f"  wrote: robots.txt, sitemap.xml ({len(all_paths)} urls), _redirects")

def write_favicon():
    """Bespoke SVG favicon — burnt orange M monogram on paper background."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#f7f3ee"/><rect x="2" y="2" width="60" height="60" fill="none" stroke="#1d2942" stroke-width="2"/><text x="32" y="44" font-family="serif" font-size="36" font-weight="700" text-anchor="middle" fill="#1d2942">M</text><line x1="10" y1="54" x2="54" y2="54" stroke="#d96b3a" stroke-width="2"/></svg>"""
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    print("  wrote: favicon.svg")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print(f"BUILDING: {BRAND}")
    print(f"DESIGN:   Workbench Blueprint")
    print(f"ROOT:     {ROOT}")
    print("=" * 60)

    # Load manifest
    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found at {MANIFEST_PATH}")
        sys.exit(1)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    manifest_by_path = {m["path"]: m for m in manifest}

    # === STEP 1: Clean ===
    print("\n[1/5] Cleaning old footprint artefacts...")
    clean_old()

    # === STEP 2: Write CSS + favicon ===
    print("\n[2/5] Writing CSS + favicon...")
    write_css()
    write_favicon()

    # === STEP 3: Render pages ===
    print("\n[3/5] Rendering pages...")
    pages_written = []

    # Home
    write("/index.html", page_home())
    pages_written.append("/")
    print(f"  / (home)")

    # /collections/ top-level index
    write("/collections/index.html", page_collections_index())
    pages_written.append("/collections/")
    print(f"  /collections/")

    # Sub-collections (filter-based pages)
    collection_filters = [
        ("union", "Union wallets", lambda c: c[1].lower().startswith("union")),
        ("poquito", "Poquito card wallets", lambda c: c[1].lower().startswith("poquito")),
        ("convoy", "Convoy iPhone cases", lambda c: "convoy" in c[1].lower()),
        ("wallets", "All wallets", lambda c: "wallet" in c[1].lower() or "bifold" in c[1].lower()),
    ]
    for slug, label, fn in collection_filters:
        write(f"/collections/{slug}/index.html", page_collection_filter(slug, label, fn))
        pages_written.append(f"/collections/{slug}/")
        print(f"  /collections/{slug}/")

    # Individual product pages — at /collections/<slug>/ (canonical), with /products/<slug>/ as a 301 via _redirects
    for slug, piece, _t, _y, _s, _img, _b in CATALOGUE:
        write(f"/collections/{slug}/index.html", page_product(slug))
        pages_written.append(f"/collections/{slug}/")
        print(f"  /collections/{slug}/  ({piece})")

    # Legacy product paths (must serve 200 because that's where backlinks point)
    # These are mirror pages — same content as the canonical, but rendered at the legacy URL
    # so that backlinks at /products/<slug>/ DO get a 200 without depending on the host honouring _redirects.
    # Note: we still ship _redirects so consolidated link equity prefers the canonical.
    LEGACY_PRODUCT_PATHS = [
        "/products/union-walnut-wallet/",
        "/products/union-wallet-in-oak/",
        "/products/union-wallet-in-cherry/",
        "/products/poquito-wallet-in-walnut/",
        "/products/poquito-wallet-in-oak/",
        "/products/convoy-iphone-6-case-in-walnut/",
    ]
    for p in LEGACY_PRODUCT_PATHS:
        slug = p.strip("/").split("/")[-1]
        # Get the canonical product HTML and re-render with a self-canonical
        html_canonical = page_product(slug)
        # Swap the canonical URL in the meta tags to point to the canonical /collections/<slug>/
        # so duplicate-content signal goes the right way
        html_legacy = html_canonical.replace(
            f'<link rel="canonical" href="{SITE_URL}/products/{slug}/">',
            f'<link rel="canonical" href="{SITE_URL}/collections/{slug}/">'
        ).replace(
            f'<meta property="og:url" content="{SITE_URL}/products/{slug}/">',
            f'<meta property="og:url" content="{SITE_URL}/collections/{slug}/">'
        )
        # The canonical in our render_page is based on `path` arg which we passed as /collections/<slug>/
        # so html_canonical already canonicalises to /collections/ — we just write the same content at the legacy path
        write(p, html_canonical)
        pages_written.append(p)
        print(f"  {p}  (legacy mirror)")

    # Legacy nested-collection mirror paths
    LEGACY_NESTED_MIRRORS = {
        "/collections/all/products/poquito-wallet-in-walnut/": "poquito-wallet-in-walnut",
        "/collections/all/products/union-walnut-wallet/": "union-walnut-wallet",
        "/collections/convoy/products/convoy-iphone-6-case-in-cherry/": "convoy-iphone-6-case-in-cherry",
        "/collections/poquito/products/poquito-wallet-in-cherry/": "poquito-wallet-in-cherry",
        "/collections/union/products/union-walnut-wallet/": "union-walnut-wallet",
        "/collections/wallets/products/union-wallet-in-cherry/": "union-wallet-in-cherry",
        "/collections/wallets/products/union-wallet-in-oak/": "union-wallet-in-oak",
        "/collections/wallets/products/union-walnut-wallet/": "union-walnut-wallet",
    }
    for path, slug in LEGACY_NESTED_MIRRORS.items():
        write(path, page_product(slug))
        pages_written.append(path)
        print(f"  {path}  (nested mirror -> {slug})")

    # /collections/all/ — Shopify-style index, serve as the catalogue itself
    write("/collections/all/index.html", page_collections_index())
    pages_written.append("/collections/all/")
    print("  /collections/all/  (catalogue mirror)")

    # /union/ legacy shortcut (21 backlinks)
    union_redirect_html = render_page(
        title="Union wallets",
        description="The Union wallet was the first piece in the Madera Woodworks Co catalogue. View the variants in walnut, oak and cherry.",
        path="/union/",
        body_html=f"""<section class="wb__main">
  <div class="wb__section">
    <div class="wb__section-head">
      <span class="label">§ Union</span>
      <h1>The Union wallet.</h1>
      <p class="lede">The original piece. Shipped in 2014, retired in 2017.</p>
    </div>
    <div class="wb__prose">
      <p>The Union was the first wallet we ever made. Two halves of book matched hardwood, an extending internal elastic, an external band, and an interior lining stitched in waxed cotton. It went through three timber variants over four years.</p>
      <p>The full Union family is in the <a href="/collections/union/">Union collection</a>, and the design retrospective is in <a href="/journal/the-poquito-design-story/">the journal</a>.</p>
    </div>
  </div>
</section>""",
    )
    write("/union/index.html", union_redirect_html)
    pages_written.append("/union/")
    print("  /union/")

    # Journal index
    write("/journal/index.html", page_journal_index())
    pages_written.append("/journal/")
    print("  /journal/")

    # Journal articles — migrate body content from manifest
    for slug, iso, date_display, title in JOURNAL_INDEX:
        m = manifest_by_path.get(f"/journal/{slug}/index.html")
        if not m:
            print(f"  WARNING: no manifest entry for journal/{slug} — using stub")
            body_html = f"""<h1>{title}</h1>
<p class="lede">Originally published {date_display}.</p>
<p>This article was part of the {BRAND} workshop journal. The full content is being restored.</p>"""
            desc = f"Workshop note from the Madera Woodworks Co journal, {date_display}."
        else:
            body_html = migrate_body(m["body"])
            desc = m["description"] or f"Workshop note from the Madera Woodworks Co journal, {date_display}."
            # Rebrand
            desc = desc.replace("Madera Woodcraft", BRAND)
        write(f"/journal/{slug}/index.html", page_journal_article(slug, body_html, title, desc))
        pages_written.append(f"/journal/{slug}/")
        print(f"  /journal/{slug}/")

    # Static pages — /pages/about/, /pages/contact-us/, /pages/privacy/
    static_pages = [
        ("about", "About the workshop", "Madera Woodworks Co was a one person studio in Sydney's inner west making hardwood wallets and iPhone cases between 2014 and 2018. About the workshop, the makers, and how the archive came to exist."),
        ("contact-us", "Contact", f"Contact details for the {BRAND} workshop archive. The workshop is closed, but emails are still answered."),
        ("privacy", "Privacy", f"Privacy notice for the {BRAND} archive website. How visitor data is handled."),
    ]
    for slug, title, desc in static_pages:
        m = manifest_by_path.get(f"/pages/{slug}/index.html")
        if not m or not m["body"]:
            # Stub fallback
            if slug == "about":
                body_html = f"""<h1>About {BRAND}</h1>
<p class="lede">A one person hardwood studio in Sydney's inner west, 2014 to 2018.</p>
<p>{BRAND} began with a single offcut of American walnut and a half formed idea that a wallet should feel like a tool, not an accessory. Over the next four years we shipped nine designs in four timber species from a shared shed in Marrickville.</p>
<p>The workshop closed in 2018 when the lease ended and the timber supplier we relied on shut up shop. This archive exists so the work has a home. Read the <a href="/journal/why-we-stopped-selling-wooden-wallets-2018-retrospective/">2018 retrospective</a> for the full story.</p>
<h2>The maker</h2>
<p>Every piece on this archive was made by hand in Sydney. We never wholesaled, never ran a sale, and never made the same piece twice in quite the same way.</p>
<h2>The archive</h2>
<p>This site documents every piece that left the bench. Browse the <a href="/collections/">full catalogue</a>, read the <a href="/journal/">journal</a>, or <a href="/pages/contact-us/">write in</a> if you own a piece and want to know its batch.</p>"""
            elif slug == "contact-us":
                body_html = f"""<h1>Contact</h1>
<p class="lede">The workshop is closed. Emails are still answered, slowly.</p>
<p>The most useful way to reach the archive is by email. Owners of existing pieces with questions about batches, finish or repair, get priority.</p>
<h2>Email</h2>
<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<h2>Instagram</h2>
<p>The archive Instagram is at <a href="{INSTAGRAM_URL}" rel="noopener">{INSTAGRAM}</a>. Older posts cover the active workshop years.</p>
<h2>Post</h2>
<p>Inner West Sydney, Australia. Specific address by email only.</p>
<h2>What we do not do</h2>
<ul>
  <li>New commissions or batches. The workshop is closed.</li>
  <li>Wholesale enquiries.</li>
  <li>Refinish work on pieces from other makers.</li>
</ul>"""
            else:
                body_html = f"""<h1>Privacy</h1>
<p class="lede">A short note about how this archive handles visitor data.</p>
<p>{BRAND} is a static archive site. The site itself does not collect personal information, run advertising trackers, or set persistent cookies beyond what the host's CDN may use for caching.</p>
<h2>Email enquiries</h2>
<p>If you email <a href="mailto:{EMAIL}">{EMAIL}</a>, your email address and message are kept for as long as needed to reply, and not shared.</p>
<h2>Analytics</h2>
<p>Basic, anonymised visitor counts are kept via the host's standard server logs. No third party analytics scripts run on this site.</p>"""
        else:
            body_html = migrate_body(m["body"])
        write(f"/pages/{slug}/index.html", page_static(slug, body_html, title, desc))
        pages_written.append(f"/pages/{slug}/")
        print(f"  /pages/{slug}/")

    # 404
    write("/404.html", page_404())
    print("  /404.html")

    # === STEP 4: Write sitemap, robots, redirects ===
    print("\n[4/5] Writing site meta...")
    write_robots_sitemap_redirects(pages_written)

    # === STEP 5: Summary ===
    print("\n[5/5] Build complete.")
    print(f"\n  Pages rendered: {len(pages_written)}")
    print(f"  CSS path:       {CSS_PATH}")
    print(f"  Brand:          {BRAND}")
    print(f"  Schema:         Organization on home, Product on collections, Article on journal")

    return pages_written


if __name__ == "__main__":
    main()
