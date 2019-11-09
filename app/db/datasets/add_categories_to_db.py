from app.db.models import Category
from app.db.config import transaction

CATEGORIES_FILE = "he_books_categories.txt"

categories = []

with open(CATEGORIES_FILE, "r") as dataset:
    categories = dataset.readlines()

with transaction() as session:
    for category in categories:
        print(category)
        print(session.add(Category(name=category)))
    session.commit()
    print(session.query(Category).all())