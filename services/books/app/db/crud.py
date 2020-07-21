"""Books CRUD db operations."""

from app.db.tables import Book


def get_all_books(session):
    """Get all books from DB.

    Args:
       session (Session): DB session.

    Returns:
        list. Book objects.

    Notes:
        Internal endpoint for tests.
    """
    return session.query(Book).all()


def add_book(session, name, author, user_id, description, publication_date,
             categories_ids):
    """Add new book to the DB.

    Args:

    Returns:
        Book. New book object.
    """
    new_book = Book(name=name,
                    author=author,
                    user_id=user_id,
                    description=description,
                    publication_date=publication_date,
                    categories_ids=categories_ids)

    session.add(new_book)
    session.commit()
    # Retrieving new data like generated id.
    session.refresh(new_book)
    return new_book


def delete_book(session, id: int):
    """Delete specific book.

    Args:
        id (int): Book id.
        session (Session): DB session.

    Returns:
        bool. If the book was found and deleted or not.
    """
    book = session.query(Book).filter_by(id=id).first()
    if book is None:
        return False

    session.delete(book)
    session.commit()
    return True


def get_book_by_id(session, id: str):
    """Get specific book by id.

    Args:
        id (int): Book id.
        session (Session): DB session.

    Returns:
        Book. Founded book.
    """
    return session.query(Book).filter_by(id=id).first()


def get_books_by_user_id(session, user_id: str):
    """Get specific book by user_id.

    Args:
        user_id (int): User id.
        session (Session): DB session.

    Returns:
        Book. Founded books.
    """
    return session.query(Book).filter_by(user_id=user_id).all()


def get_category_books_by_user_id(session, user_id: str, category_id: list):
    """Get specific book by user_id.

    Args:
        user_id (int): User id.
        session (Session): DB session.
        category_id (int): Specific category id.

    Returns:
        Book. Founded books.
    """
    return session.query(Book).filter_by(user_id=user_id).filter(
        Book.categories_ids.contains(category_id)).all()


def get_books_by_name(session, filter: str):
    """Get all books that match to specific name filter from DB.

    Args:
        filter (str): Contains filter.
        session (Session): Current DB session.

    Returns:
        list. Filtered books.
    """
    return session.query(Book).filter(Book.name.contains(filter)).all()
