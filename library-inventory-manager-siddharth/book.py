from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"   # "available" or "issued"

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def issue(self) -> bool:
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self) -> bool:
        return self.status == "available"
