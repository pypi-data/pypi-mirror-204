from typing import Any

from pydantic import FilePath

from scribber.core.document import Title, Paragraph, EmptyLine, Table, Builder, CodeBlock


class TextDocument:
    def __init__(self) -> None:
        self.parts = []
        self._report = ""
        self._line_brake = "\n"
        self._line_divider = "-"
        self._col_divider = "|"

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def _render_title(self, title: Title) -> None:
        str_len = len(title.title)
        self._report += title.title + self._line_brake
        self._report += "=" * str_len + self._line_brake

    def get_result(self) -> str:
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
        return self._report

    def save(self, filename: FilePath):
        with open(filename, "w") as f:
            f.write(self.get_result())

    def _render_paragraph(self, paragraph: Paragraph):
        self._report += paragraph.text + self._line_brake

    def _render_code_block(self, code_block: CodeBlock):
        self._report += code_block.code + self._line_brake

    def _render_brake(self):
        self._report += self._line_brake

    def _render_table(self, item):
        col_length = []
        col_count = len(item.headers)
        sep_count = col_count - 1 if col_count > 1 else 1
        for itm in item.headers:
            col_length.append(len(itm) + 2)
        col = 0
        for itm in item.headers:
            column_content_length = max([len(str(_[col])) for _ in item.content])
            if col_length[col] < column_content_length + 2:
                col_length[col] = column_content_length + 2
            col += 1
        table_line_separator = (
            self._line_divider * (sum(col_length) + sep_count) + self._line_brake
        )
        self._report += table_line_separator
        headers_justified = []
        i = 0
        for itm in item.headers:
            headers_justified.append(f"{itm : ^{col_length[i]}}")
            i += 1
        self._report += self._col_divider.join(headers_justified) + self._line_brake
        self._report += table_line_separator

        for line in item.content:
            i = 0
            content_justified = []
            for itm in item.headers:
                content_justified.append(f"{str(line[i]) : ^{col_length[i]}}")
                i += 1
            self._report += self._col_divider.join(content_justified) + self._line_brake
        self._report += table_line_separator


class TextDocumentBuilder(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._text_report = TextDocument()

    @property
    def parts(self) -> TextDocument:
        parts = self._text_report
        self.reset()
        return parts

    def add_title(self, title: Title) -> None:
        self._text_report.add(title)

    def add_table(self, table: Table) -> None:
        self._text_report.add(table)

    def add_paragraph(self, paragraph: Paragraph) -> None:
        self._text_report.add(paragraph)

    def add_brake(self):
        self._text_report.add(EmptyLine())

    def add_code_block(self, code_block: CodeBlock):
        self._text_report.add(code_block)
