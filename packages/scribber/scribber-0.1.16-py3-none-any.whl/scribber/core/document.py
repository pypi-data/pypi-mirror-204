from abc import ABC, abstractmethod
from typing import Any, Optional, List, Iterable
from pydantic import BaseModel, validator, FilePath


class Title(BaseModel):
    title: str
    level: int = 1

    @validator("title")
    def title_not_empty(cls, v):
        assert len(v) > 0, "must be one or more symbols"
        return v

    @validator("level")
    def level_in_range(cls, v):
        assert 0 < v <= 6, "must be in 1..6 range"
        return v


class Paragraph(BaseModel):
    text: str

    @validator("text")
    def field_not_empty(cls, v):
        assert len(v) > 0, "must be one or more symbols"
        return v


class CodeBlock(BaseModel):
    code: str
    style: str

    @validator("code")
    def field_not_empty(cls, v):
        assert len(v) > 0, "must be one or more symbols"
        return v


class Table(BaseModel):
    headers: List[str]
    content: List[Any]

    @validator("headers", "content")
    def not_empty(cls, v):
        assert len(v) > 0, "must not be empty"
        return v


class EmptyLine(BaseModel):
    pass


class SimpleDocument:
    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def get_result(self) -> List[Any]:
        return self.parts


class Builder(ABC):
    @property
    @abstractmethod
    def parts(self) -> None:
        pass

    @abstractmethod
    def add_title(self, title: Title) -> None:
        pass

    @abstractmethod
    def add_table(self, table: Table) -> None:
        pass

    @abstractmethod
    def add_paragraph(self, paragraph: Paragraph) -> None:
        pass

    @abstractmethod
    def add_code_block(self, code_block: CodeBlock) -> None:
        pass

    @abstractmethod
    def add_brake(self):
        pass


class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> None:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_report_from_doc(self, doc: SimpleDocument):
        for item in doc.get_result():
            if isinstance(item, Title):
                self.builder.add_title(item)
            elif isinstance(item, Paragraph):
                self.builder.add_paragraph(item)
            elif isinstance(item, EmptyLine):
                self.builder.add_brake()
            elif isinstance(item, Table):
                self.builder.add_table(item)
            elif isinstance(item, CodeBlock):
                self.builder.add_code_block(item)
