from scribber.core.document import (
    SimpleDocument,
    Title,
    EmptyLine,
    Paragraph,
    Table,
    Director,
    CodeBlock,
)
from scribber.formats.excel.excel_document import ExcelDocumentBuilder
from scribber.formats.markdown.markdown_document import MarkdownDocumentBuilder
from scribber.formats.text.text_document import TextDocumentBuilder
from scribber.formats.word.word_document import WordDocumentBuilder

CODE_EXAMPLE = """
import platform

def main():
    print("Hello World!")
    print(f"OS: {platform.system()}")
    
if __name__ == "__main__":
    main()             
"""

CODE_RESULT = """Hello World!
OS: Linux"""


if __name__ == "__main__":
    # Create abstract document
    doc = SimpleDocument()
    doc.add(Title(title="Funny report"))
    doc.add(EmptyLine())
    doc.add(Paragraph(text="Let me show you report"))
    doc.add(
        Table(
            headers=["one", "two", "three", "four"],
            content=[
                (1, 2, 3, 4),
                ("234", 345, 986, ""),
                (89, 35, 587643, 8675),
            ],
        )
    )
    doc.add(EmptyLine())
    doc.add(Title(title="Code block", level=2))
    doc.add(CodeBlock(style="python", code=CODE_EXAMPLE))
    doc.add(CodeBlock(style="console", code=CODE_RESULT))
    doc.add(Paragraph(text="It's Ok!"))

    director = Director()
    text_report_builder = TextDocumentBuilder()
    word_report_builder = WordDocumentBuilder()
    excel_report_builder = ExcelDocumentBuilder()
    marckdown_report_builder = MarkdownDocumentBuilder()

    print("Make a Text Document")
    director.builder = text_report_builder
    director.build_report_from_doc(doc)
    text_report_builder.parts.save("test.txt")

    print("Make a Word Document")
    director.builder = word_report_builder
    director.build_report_from_doc(doc)
    word_report_builder.parts.save("test.docx")

    print("Make a Excel Document")
    director.builder = excel_report_builder
    director.build_report_from_doc(doc)
    excel_report_builder.parts.save("test.xlsx")

    print("Make a Marckdown Document")
    director.builder = marckdown_report_builder
    director.build_report_from_doc(doc)
    marckdown_report_builder.parts.save("test.md")

    print()
    print("Build without Director")
    text_report_builder.add_title(Title(title="Next report"))
    text_report_builder.add_paragraph(Paragraph(text="That is all!"))
    print(text_report_builder.parts.get_result())
