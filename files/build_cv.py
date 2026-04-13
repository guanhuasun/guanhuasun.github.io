"""
Compile CV.md to CV.pdf using fpdf2's write_html for proper text wrapping.

Usage:
    python build_cv.py

Reads CV.md from the same directory and writes CV.pdf alongside it.
"""

import os
import re
from fpdf import FPDF

DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DIR, "CV.md")
PDF_PATH = os.path.join(DIR, "CV.pdf")

FONTS_DIR = "C:/Windows/Fonts"


class CVPDF(FPDF):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_font("TNR", "",  os.path.join(FONTS_DIR, "times.ttf"))
        self.add_font("TNR", "B", os.path.join(FONTS_DIR, "timesbd.ttf"))
        self.add_font("TNR", "I", os.path.join(FONTS_DIR, "timesi.ttf"))
        self.add_font("TNR", "BI", os.path.join(FONTS_DIR, "timesbi.ttf"))

    def header(self):
        pass

    def footer(self):
        pass


def md_inline_to_html(text):
    """Convert markdown inline formatting to HTML."""
    # Links: [text](url) -> <a href="url"><font color="#1a5276">text</font></a>
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2"><font color="#1a5276">\1</font></a>',
        text
    )
    # Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic: *text* -> <i>text</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # <u> tags pass through to HTML as-is
    return text


def build_pdf():
    with open(MD_PATH, encoding="utf-8") as f:
        lines = f.read().splitlines()

    pdf = CVPDF(format="letter")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margin(22)
    pdf.add_page()
    pdf.set_text_color(34, 34, 34)
    pdf.set_font("TNR", "", 10.5)

    L_MARGIN = pdf.l_margin
    PAGE_W = pdf.w - pdf.l_margin - pdf.r_margin

    in_header = True

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

        # Skip empty lines
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # H1: name
        if stripped.startswith("# ") and not stripped.startswith("## "):
            text = stripped[2:]
            pdf.set_font("TNR", "B", 22)
            pdf.cell(0, 10, text, align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("TNR", "", 10.5)
            i += 1
            continue

        # Horizontal rule
        if stripped == "---":
            in_header = False
            pdf.set_draw_color(100, 100, 100)
            y = pdf.get_y()
            pdf.line(L_MARGIN, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
            i += 1
            continue

        # Centered header lines (affiliation, email)
        if in_header:
            pdf.set_font("TNR", "", 10.5)
            pdf.cell(0, 5, stripped, align="C", new_x="LMARGIN", new_y="NEXT")
            i += 1
            continue

        # H2: section header
        if stripped.startswith("## ") and not stripped.startswith("### "):
            text = stripped[3:]
            pdf.ln(3)
            pdf.set_font("TNR", "B", 13)
            pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(100, 100, 100)
            y = pdf.get_y()
            pdf.line(L_MARGIN, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
            pdf.set_font("TNR", "", 10.5)
            i += 1
            continue

        # H3: subsection header
        if stripped.startswith("### "):
            text = stripped[4:]
            pdf.ln(1)
            pdf.set_font("TNR", "B", 11)
            pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            pdf.set_font("TNR", "", 10.5)
            i += 1
            continue

        # Ordered list item
        m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m:
            num = m.group(1)
            text = m.group(2)
            # Gather continuation lines
            while i + 1 < len(lines):
                ns = lines[i + 1].strip()
                if not ns or re.match(r'^\d+\.\s', ns) or ns.startswith(("- ", "#")):
                    break
                i += 1
                text += " " + ns

            html = md_inline_to_html(text)
            indent = 12
            num_w = 8

            # Print number
            pdf.set_font("TNR", "", 10.5)
            pdf.set_x(L_MARGIN + indent - num_w)
            pdf.cell(num_w, 5, f"{num}.", new_x="END")

            # Print content with hanging indent using write_html
            x_start = L_MARGIN + indent
            content_w = PAGE_W - indent
            pdf.set_x(x_start)
            pdf.set_font("TNR", "", 10.5)
            # Use multi_cell approach: save position, set temporary margin
            old_l_margin = pdf.l_margin
            pdf.l_margin = x_start
            pdf.write_html(f'<font face="TNR" size="10">{html}</font>')
            pdf.l_margin = old_l_margin
            pdf.ln(2)
            i += 1
            continue

        # Unordered list item
        if stripped.startswith("- "):
            text = stripped[2:]
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and not lines[i + 1].strip().startswith("- "):
                i += 1
                text += " " + lines[i].strip()

            html = md_inline_to_html(text)
            indent = 12
            bullet_w = 6

            pdf.set_font("TNR", "", 10.5)
            pdf.set_x(L_MARGIN + indent - bullet_w)
            pdf.cell(bullet_w, 5, "\u2022", new_x="END")

            x_start = L_MARGIN + indent
            old_l_margin = pdf.l_margin
            pdf.l_margin = x_start
            pdf.write_html(f'<font face="TNR" size="10">{html}</font>')
            pdf.l_margin = old_l_margin
            pdf.ln(2)
            i += 1
            continue

        # Regular paragraph
        para = stripped
        while i + 1 < len(lines):
            ns = lines[i + 1].strip()
            if not ns or ns.startswith(("#", "-", "---")) or re.match(r'^\d+\.\s', ns):
                break
            i += 1
            para += " " + ns

        html = md_inline_to_html(para)
        pdf.set_font("TNR", "", 10.5)
        pdf.write_html(f'<font face="TNR" size="10">{html}</font>')
        pdf.ln(4)
        i += 1

    pdf.output(PDF_PATH)
    print(f"Written: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
