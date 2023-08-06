from typing import Any

from pydantic import FilePath

from scribber.core.document import Title, Paragraph, EmptyLine, Table, Builder, CodeBlock

import xlsxwriter


class ExcelDocument:
    def __init__(self) -> None:
        self._row = 0
        self._col = 0
        self.parts = []
        self._workbook = xlsxwriter.Workbook()
        self._report = self._workbook.add_worksheet()
        self._bold_format = self._workbook.add_format({'bold': True})

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def _render_title(self, title: Title) -> None:
        self._report.write(self._row, self._col, title.title, self._bold_format)
        self._row += 1

    def get_result(self) -> xlsxwriter.Workbook:
        for item in self.parts:
            if isinstance(item, Title):
                self._render_title(item)
            elif isinstance(item, Paragraph):
                self._render_paragraph(item)
            elif isinstance(item, EmptyLine):
                self._render_brake()
            elif isinstance(item, Table):
                self._render_table(item)
            elif isinstance(item, CodeBlock):
                self._render_code_block(item)
        return self._workbook

    def save(self, filename: FilePath):
        self._workbook.filename = filename
        self.get_result().close()

    def _render_paragraph(self, paragraph: Paragraph):
        self._report.write(self._row, self._col, paragraph.text)
        self._row += 1

    def _render_code_block(self, code_block: CodeBlock):
        for line in code_block.code.split(sep="\n"):
            self._report.write(self._row, self._col, line)
            self._row += 1

    def _render_brake(self):
        self._row += 1

    def _render_table(self, item):
        for header in item.headers:
            self._report.write(self._row, self._col, header, self._bold_format)
            self._col += 1
        self._row += 1
        self._col = 0

        for row in item.content:
            for itm in row:
                self._report.write(self._row, self._col, itm)
                self._col += 1
            self._col = 0
            self._row += 1


class ExcelDocumentBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._excel_report = ExcelDocument()

    @property
    def parts(self) -> ExcelDocument:
        parts = self._excel_report
        self.reset()
        return parts

    def add_title(self, title: Title) -> None:
        self._excel_report.add(title)

    def add_table(self, table: Table) -> None:
        self._excel_report.add(table)

    def add_paragraph(self, paragraph: Paragraph) -> None:
        self._excel_report.add(paragraph)

    def add_brake(self):
        self._excel_report.add(EmptyLine())

    def add_code_block(self, code_block: CodeBlock):
        self._excel_report.add(code_block)
