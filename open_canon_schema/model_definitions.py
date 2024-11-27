"""Model definitions for the Open Canon Schema.

The Open Canon Schema is a data model for representing the text of scripture in a machine-readable format. The schema is
designed to be flexible and extensible.
"""
from __future__ import annotations
import pydantic
import warnings
from typing_extensions import Self


class Verse(pydantic.BaseModel):
    """A verse of scripture."""

    text: str = pydantic.Field(description="The text of the verse.")
    footnotes: dict[str, str] | None = pydantic.Field(
        description="A dictionary of footnotes, where the key is the footnote reference and the value is the footnote"
        "text. Footnote references in the text follow extended markdown syntax, e.g. [^1], and the keys of the "
        "footnotes attribute are the footnote label. For example, if the text of the verse is 'This is a verse[^1].', "
        "the footnotes attribute would be {'1': 'This is a footnote.'}."
    )

    @pydantic.model_validator(mode="after")
    def validate_footnotes(self) -> Self:
        """Warn if a footnote key is not found in the verse text."""
        if self.footnotes is None:
            return self
        for key in self.footnotes.keys():
            if f"[^{key}]" not in self.text:
                warnings.warn(f"Footnote key '{key}' not found in verse text.")
        return self


class Chapter(pydantic.BaseModel):
    """A chapter of scripture."""

    title: str | None = pydantic.Field(description="The title of the chapter.")
    header: str | None = pydantic.Field(description="The header of the chapter.")
    verses: dict[str, Verse] = pydantic.Field(
        description="A dictionary of verses, where the key is the verse number and the value is the verse."
    )


class Section(pydantic.BaseModel):
    """A section of scripture.

    A section of scripture is a collection of chapters that are grouped together for a specific purpose by the original
    author. Examples include Mormon's grouping of the chapters about the Sons of Mosiah in Alma or the grouping of
    chapters about Samuel the Lamanite in Helaman.
    """

    title: str | None = pydantic.Field(description="The title of the section.")
    header: str | None = pydantic.Field(description="The header of the section.")
    chapters: list[Chapter] = pydantic.Field(
        description="A list of chapters in the section."
    )


class Book(pydantic.BaseModel):
    """A book of scripture.

    A book of scripture is a collection of chapters that may or may not be divided into sections. Generally, a book is
    written by a single author or a small group of authors, and is considered a single work. Generally, a book can
    stand alone as a complete work, but may be part of a larger volume of scripture. Examples include Genesis, Exodus,
    1 Nephi, Alma, Joseph Smith—Matthew.
    """

    title: str = pydantic.Field(
        description="The title of the book.",
        examples=["Genesis", "Exodus", "Leviticus", "Alma", "Doctrine and Covenants"],
    )
    chapters: dict[str, Chapter] = pydantic.Field(
        description="A dictionary of chapters, where the key is the chapter title and the value is the chapter."
    )
    sections: dict[str, Section] | None = pydantic.Field(
        description="A dictionary of sections, where the key is the section title and the value is the section."
    )
    short_title: str | None = pydantic.Field(
        description="A short title of the book.",
        examples=["Gen", "Exo", "Lev", "Alma", "D&C"],
    )


class Volume(pydantic.BaseModel):
    """A volume of books.

    A volume is a collection of individual books that have been compiled into a single, larger work.
    """

    title: str = pydantic.Field(
        description="The title of the volume.",
        examples=[
            "Old Testament",
            "New Testament",
            "Book of Mormon",
            "Doctrine and Covenants",
            "Pearl of Great Price",
        ],
    )
    books: dict[str, Book] = pydantic.Field(
        description="A dictionary of books, where the key is the book title and the value is the book."
    )
