"""
This module demonstrates the use of SQLAlchemy's Core functionality for
 building and executing database queries.
The example shows how to define table schemas and perform queries using the
 SQLAlchemy Core expression language.
It provides functionality to query books based on author names from a
 structured database.
"""

from typing import Any, Sequence

from sqlalchemy import (
    Column,
    Engine,
    ForeignKey,
    Integer,
    MetaData,
    Row,
    Select,
    String,
    Table,
    create_engine,
    select,
)

engine: Engine = create_engine(
    "mysql+pymysql://user:password@server/database",
)
metadata: MetaData = MetaData()
authors: Table = Table(
    "authors",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "name",
        String,
    ),
)
books: Table = Table(
    "books",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column(
        "title",
        String,
    ),
    Column(
        "author_id",
        Integer,
        ForeignKey("authors.id"),
    ),
    Column(
        "year",
        Integer,
    ),
)


def fetch_books_by_author(
    author_name: str,
) -> Sequence[Row[Any]]:
    """
    Retrieves all books written by the specified author.
    :param author_name: The name of the author whose books to find.
    :type author_name: str
    :return: A list of all books from the given author name
    :rtype: Sequence[Row[Any]]
    """
    select_statement: Select[Any] = (
        select([books.c.title, books.c.year])  # type: ignore
        .select_from(books.join(authors))
        .where(authors.c.name == author_name)
    )
    with engine.connect() as connection:
        return connection.execute(
            select_statement,
        ).fetchall()


books_by_author: list[Row[Table]] = list(  # type: ignore
    fetch_books_by_author("Gabriel García Márquez")
)
for book in books_by_author:
    print(book)
