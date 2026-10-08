"""
build_pdfs.py
-------------
Turns the Markdown reports into PDFs.

    reports/policy_brief.md   -> reports/policy_brief.pdf
    reports/working_paper.md  -> reports/working_paper.pdf

Pure Python, no external programs:
  1. markdown converts the .md text to HTML (with the "tables" and
     "fenced_code" extensions, so tables and the formula block render).
  2. xhtml2pdf lays that HTML out as a PDF, using the CSS below.

Two details matter on this project:
  - Fonts. The PDF's built-in fonts can't draw ₦, − (minus) or ≥, so a
    Windows font that has them is embedded (see FONT_CANDIDATES). xhtml2pdf
    only uses fonts declared in the CSS with @font-face, so that is how they
    are added; reportlab is used only to check each font has the glyphs.
  - File access. xhtml2pdf only reads files inside the document's own
    folder unless told otherwise, which blocks the Windows fonts folder. POLICY
    allows the project folder and the fonts folder, and nothing else.
  - Images. The reports link charts with relative paths such as
    ../outputs/figures/png/queue_cap.png. xhtml2pdf calls link_callback for
    each one, and we turn it into a full path on disk.
  - An image bug. xhtml2pdf 0.2.23 names each image after the memory address
    of a short-lived object. Python reuses that address for the next image,
    so every image got the same name and the PDF repeated the first one.
    _image_name below names each image by a hash of its pixels instead.

Run from the project root:
    python src/build_pdfs.py
"""

import hashlib
import pathlib
import re

import markdown
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from xhtml2pdf import xhtml2pdf_reportlab
from xhtml2pdf.config.resources import ResourceAccessPolicy

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
REPORTS = PROJECT_ROOT / "reports"
DOCUMENTS = ["policy_brief", "working_paper"]

# Characters the reports use that a font must be able to draw.
REQUIRED_CHARS = "₦−–≥×÷≈Σ→·’"

# (family name, regular, bold, italic) - first one with every required glyph wins.
FONT_DIR = pathlib.Path(r"C:\Windows\Fonts")
FONT_CANDIDATES = [
    ("SegoeUI", "segoeui.ttf", "segoeuib.ttf", "segoeuii.ttf"),
    ("Arial", "arial.ttf", "arialbd.ttf", "ariali.ttf"),
    ("Calibri", "calibri.ttf", "calibrib.ttf", "calibrii.ttf"),
]
MONO_CANDIDATES = [("Consolas", "consola.ttf"), ("CourierNew", "cour.ttf")]


def has_glyphs(path: pathlib.Path, chars: str) -> bool:
    """True if the TrueType font at path can draw every character in chars."""
    font = TTFont("probe", str(path))
    return all(ord(c) in font.face.charToGlyph for c in chars)


def font_css() -> tuple[str, str, str]:
    """Pick a body and a monospace font. Returns their family names and the @font-face CSS that embeds them."""
    body = next((c for c in FONT_CANDIDATES
                 if all((FONT_DIR / f).exists() for f in c[1:]) and has_glyphs(FONT_DIR / c[1], REQUIRED_CHARS)), None)
    mono = next((c for c in MONO_CANDIDATES
                 if (FONT_DIR / c[1]).exists() and has_glyphs(FONT_DIR / c[1], REQUIRED_CHARS)), None)
    if body is None or mono is None:
        raise RuntimeError(f"No installed font can draw all of {REQUIRED_CHARS!r}")
    family, regular, bold, italic = body

    def face(name, file, weight="normal", style="normal"):
        # Forward slashes: the path goes inside CSS url(), where backslashes are escapes.
        url = (FONT_DIR / file).as_posix()
        return f"@font-face {{ font-family: {name}; src: url('{url}'); font-weight: {weight}; font-style: {style}; }}\n"

    css = (face(family, regular) + face(family, bold, weight="bold") + face(family, italic, style="italic")
           + face(mono[0], mono[1]))
    return family, mono[0], css


CSS = """
{faces}
@page {{ size: A4; margin: 2cm 2cm 2cm 2cm;
         @frame footer {{ -pdf-frame-content: footer; bottom: 0.8cm; margin-left: 2cm; margin-right: 2cm; height: 1cm; }} }}
body  {{ font-family: {body}; font-size: 10pt; line-height: 1.4; color: #0b0b0b; }}
h1    {{ font-size: 18pt; line-height: 1.2; margin: 0 0 6pt 0; }}
h2    {{ font-size: 13pt; margin: 14pt 0 4pt 0; }}
h3    {{ font-size: 11pt; margin: 10pt 0 3pt 0; }}
h4    {{ font-size: 10pt; margin: 8pt 0 2pt 0; }}
p     {{ margin: 0 0 6pt 0; }}
li    {{ margin: 0 0 3pt 0; }}
a     {{ color: #1c5cab; text-decoration: none; }}
table {{ width: 100%; margin: 4pt 0 8pt 0; }}
th    {{ background-color: #ecebe7; font-weight: bold; text-align: left; }}
th, td {{ border: 0.5pt solid #b5b4ad; padding: 3pt 4pt 2pt 4pt; font-size: 8.5pt; line-height: 1.25;
          vertical-align: top; }}
pre   {{ font-family: {mono}; font-size: 8pt; background-color: #f4f3ef; padding: 6pt; line-height: 1.3; }}
code  {{ font-family: {mono}; font-size: 8.5pt; }}
hr    {{ color: #b5b4ad; }}
img   {{ margin: 4pt 0 4pt 0; }}
#footer {{ font-size: 8pt; color: #52514e; text-align: center; }}
"""

# Folders the PDF builder may read: the project (for images) and the system fonts.
POLICY = ResourceAccessPolicy(base_dir=PROJECT_ROOT, extra_roots=(FONT_DIR,))

def _image_name(self) -> str:
    """A name that is the same only for identical pictures (see the docstring at the top)."""
    return "PmlImage_" + hashlib.md5(self.getRGBData()).hexdigest()


# reportlab calls str() on the image to decide whether it has drawn it before.
xhtml2pdf_reportlab.PmlImageReader.__str__ = _image_name

# Usable page width (A4 210 mm minus 2 x 20 mm margins), in points: 170 mm = 482 pt.
IMAGE_WIDTH_PT = 482


def link_callback(uri: str, rel: str, base: pathlib.Path) -> str:
    """Resolve an image path from the Markdown into a file on disk; leave web links alone."""
    if uri.startswith(("http://", "https://", "mailto:", "data:")):
        return uri
    path = (base / uri).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image or link not found: {uri} -> {path}")
    return str(path)


def build(name: str, body_font: str, mono_font: str, faces: str) -> pathlib.Path:
    md_path = REPORTS / f"{name}.md"
    html_body = markdown.markdown(md_path.read_text(encoding="utf-8"), extensions=["tables", "fenced_code", "sane_lists"])
    # Scale every image to the page width; xhtml2pdf ignores CSS max-width.
    html_body = re.sub(r"<img ", f'<img width="{IMAGE_WIDTH_PT}" ', html_body)
    title = re.search(r"<h1>(.*?)</h1>", html_body).group(1)
    html = (f"<html><head><meta charset='utf-8'><title>{title}</title>"
            f"<style>{CSS.format(faces=faces, body=body_font, mono=mono_font)}</style></head><body>"
            f"<div id='footer'>{title} · page <pdf:pagenumber/> of <pdf:pagecount/></div>"
            f"{html_body}</body></html>")
    pdf_path = REPORTS / f"{name}.pdf"
    with pdf_path.open("wb") as f:
        result = pisa.CreatePDF(html, dest=f, encoding="utf-8", resource_policy=POLICY,
                                link_callback=lambda uri, rel: link_callback(uri, rel, md_path.parent))
    if result.err:
        raise RuntimeError(f"xhtml2pdf reported {result.err} error(s) for {name}")
    return pdf_path


def main() -> None:
    body_font, mono_font, faces = font_css()
    print(f"Fonts: body {body_font}, monospace {mono_font}")
    for name in DOCUMENTS:
        print(f"Saved {build(name, body_font, mono_font, faces).relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
