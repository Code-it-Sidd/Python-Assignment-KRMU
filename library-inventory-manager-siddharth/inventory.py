from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List, Optional

from .book import Book

logger = logging.getLogger(__name__)


class LibraryInventory:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.books: List[Book] = []
        self.load_from_file()

    # ------------ core operations ------------

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        logger.info("Book added: %s", book)
        self.save_to_file()

    def search_by_title(self, title: str) -> List[Book]:
        title_lower = title.lower()
        return [b for b in self.books if title_lower in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[Book]:
        return list(self.books)

    # ------------ JSON persistence ------------

    def save_to_file(self) -> None:
        try:
            data = [book.to_dict() for book in self.books]
            contents = json.dumps(data, indent=2)
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(contents, encoding="utf-8")
            logger.info("Saved %d books to %s", len(self.books), self.storage_path)
        except (OSError, TypeError, ValueError) as exc:
            logger.error("Failed to save inventory: %s", exc)

    def load_from_file(self) -> None:
        if not self.storage_path.exists():
            logger.info("Storage file %s does not exist, starting empty", self.storage_path)
            self.books = []
            return
        try:
            contents = self.storage_path.read_text(encoding="utf-8")
            if not contents.strip():
                logger.info("Storage file %s is empty", self.storage_path)
                self.books = []
                return
            data = json.loads(contents)
            self.books = [
                Book(
                    title=item.get("title", ""),
                    author=item.get("author", ""),
                    isbn=item.get("isbn", ""),
                    status=item.get("status", "available"),
                )
                for item in data
            ]
            logger.info("Loaded %d books from %s", len(self.books), self.storage_path)
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.error("Failed to load inventory (corrupted/missing): %s", exc)
            self.books = []
