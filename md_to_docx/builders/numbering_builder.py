from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from ..models import DocumentMetadata


class NumberingBuilder:
    def __init__(self, doc: Document, metadata: DocumentMetadata):
        self.doc = doc
        self.metadata = metadata
        self.chapter_counters: dict[int, int] = {}
        self.current_chapter: int = 0

    def setup_heading_numbering(self):
        if not self.metadata.heading_numbering.enabled:
            return

        numbering_part = self.doc.part.numbering_part
        numbering = numbering_part._element

        abstract_num_id = self._create_abstract_numbering(numbering)
        num_id = self._create_numbering_instance(numbering, abstract_num_id)

        return num_id

    def _create_abstract_numbering(self, numbering) -> int:
        abstract_num = OxmlElement("w:abstractNum")
        abstract_num_id = 1
        abstract_num.set(qn("w:abstractNumId"), str(abstract_num_id))

        for level in range(9):
            lvl = OxmlElement("w:lvl")
            lvl.set(qn("w:ilvl"), str(level))

            start = OxmlElement("w:start")
            start.set(qn("w:val"), "1")
            lvl.append(start)

            numFmt = OxmlElement("w:numFmt")
            if level == 0:
                numFmt.set(qn("w:val"), "decimal")
            elif level <= 2:
                numFmt.set(qn("w:val"), "decimal")
            else:
                numFmt.set(qn("w:val"), "decimal")
            lvl.append(numFmt)

            lvlText = OxmlElement("w:lvlText")
            if level == 0:
                lvlText.set(qn("w:val"), "%1")
            elif level == 1:
                lvlText.set(qn("w:val"), "%1.%2")
            elif level == 2:
                lvlText.set(qn("w:val"), "%1.%2.%3")
            elif level == 3:
                lvlText.set(qn("w:val"), "%1.%2.%3.%4")
            else:
                lvlText.set(qn("w:val"), "%1.%2.%3.%4.%5")
            lvl.append(lvlText)

            lvlJc = OxmlElement("w:lvlJc")
            lvlJc.set(qn("w:val"), "left")
            lvl.append(lvlJc)

            pPr = OxmlElement("w:pPr")
            ind = OxmlElement("w:ind")
            ind.set(qn("w:left"), str(360 + level * 180))
            ind.set(qn("w:hanging"), "360")
            pPr.append(ind)
            lvl.append(pPr)

            rPr = OxmlElement("w:rPr")
            sz = OxmlElement("w:sz")
            sz.set(qn("w:val"), str(24 - level * 2))
            rPr.append(sz)
            lvl.append(rPr)

            abstract_num.append(lvl)

        numbering.append(abstract_num)
        return abstract_num_id

    def _create_numbering_instance(self, numbering, abstract_num_id: int) -> int:
        num = OxmlElement("w:num")
        num_id = 2
        num.set(qn("w:numId"), str(num_id))

        abstractNumId = OxmlElement("w:abstractNumId")
        abstractNumId.set(qn("w:val"), str(abstract_num_id))
        num.append(abstractNumId)

        numbering.append(num)
        return num_id

    def set_heading_number(self, paragraph, level: int):
        if not self.metadata.heading_numbering.enabled:
            return

        if level == 1:
            self.chapter_counters = {}
            self.current_chapter += 1
            num = self.current_chapter
        else:
            self.chapter_counters[level] = self.chapter_counters.get(level, 0) + 1
            for l in range(level + 1, 10):
                self.chapter_counters.pop(l, None)
            num = self.chapter_counters[level]
            if level == 2:
                chapter = self.current_chapter
                num = f"{chapter}.{num}"

        pPr = paragraph._element.get_or_add_pPr()
        numPr = OxmlElement("w:numPr")
        ilvl = OxmlElement("w:ilvl")
        ilvl.set(qn("w:val"), str(level - 1))
        numPr.append(ilvl)
        numId = OxmlElement("w:numId")
        numId.set(qn("w:val"), "2")
        numPr.append(numId)
        pPr.append(numPr)