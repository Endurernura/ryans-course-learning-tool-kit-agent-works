"""Build study documents from the supplied content-free Word template."""

from pathlib import Path
import re

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Twips


TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "course-study.docx"


def _element(tag, **attrs):
    item = OxmlElement(f"w:{tag}")
    for key, value in attrs.items():
        item.set(qn(f"w:{key}"), str(value))
    return item


def new_document(title, running_title=None, *, line_numbers=True):
    """Return an editable document. Add the visible title with the Title style."""
    document = Document(TEMPLATE)
    document.core_properties.title = title
    for section in document.sections:
        section.header.paragraphs[0].text = running_title or title
        if not line_numbers:
            numbering = section._sectPr.find(qn("w:lnNumType"))
            if numbering is not None:
                section._sectPr.remove(numbering)
    return document


def add_bookmark(document, paragraph, name):
    """Anchor the start of a real paragraph with a stable Word bookmark name."""
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,39}", name):
        raise ValueError(f"Invalid Word bookmark name: {name}")
    bookmarks = document.element.xpath(".//w:bookmarkStart")
    if any(mark.get(qn("w:name")) == name for mark in bookmarks):
        raise ValueError(f"Duplicate Word bookmark: {name}")
    index = 1 + max((int(mark.get(qn("w:id"))) for mark in bookmarks), default=-1)
    start = _element("bookmarkStart", id=index, name=name)
    end = _element("bookmarkEnd", id=index)
    position = 1 if paragraph._p.pPr is not None else 0
    paragraph._p.insert(position, start)
    paragraph._p.insert(position + 1, end)


def add_link(paragraph, target, label):
    """Add a styled document-internal hyperlink without an external relationship."""
    hyperlink = _element("hyperlink", anchor=target, history=1)
    run = _element("r")
    props = _element("rPr")
    props.append(_element("rStyle", val="CourseLink"))
    run.append(props)
    text = _element("t")
    text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    text.text = label
    run.append(text)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def add_question_heading(document, title, target, link_label):
    """Put a short question/answer locator on the right of a compact heading."""
    paragraph = document.add_paragraph(title, style="Question Head")
    paragraph.add_run("\t")
    add_link(paragraph, target, link_label)
    return paragraph


def add_table(document, headers, rows, widths=None, *, numeric_columns=()):
    """Build a fixed-width, repeat-header table with 12-point table text.

    Widths are relative column weights. Set numeric_columns to zero-based indices.
    """
    if not headers:
        raise ValueError("A table needs at least one column.")
    cells = [headers, *rows]
    if any(len(row) != len(headers) for row in cells):
        raise ValueError("Every table row must match the header column count.")
    weights = [1] * len(headers) if widths is None else list(widths)
    if len(weights) != len(headers) or any(weight <= 0 for weight in weights):
        raise ValueError("Each table column needs a positive width weight.")
    section = document.sections[-1]
    usable = (section.page_width - section.left_margin - section.right_margin) / 635
    widths_twips = [round(usable * weight / sum(weights)) for weight in weights]
    table = document.add_table(rows=len(cells), cols=len(headers))
    table.style = "Course Table"
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for column, width in zip(table.columns, widths_twips):
        column.width = Twips(width)
    for index, (row, values) in enumerate(zip(table.rows, cells)):
        properties = row._tr.get_or_add_trPr()
        properties.append(_element("cantSplit"))
        if index == 0:
            properties.append(_element("tblHeader"))
        for column, (cell, value, width) in enumerate(zip(row.cells, values, widths_twips)):
            cell.width = Twips(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            paragraph = cell.paragraphs[0]
            paragraph.style = "Table Text"
            if index == 0 or column in numeric_columns:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.add_run(str(value)).bold = index == 0
            if index == 0:
                cell._tc.get_or_add_tcPr().append(_element("shd", fill="EDEDED"))
    return table
