from db_models import categories, database

async def get_all_categories(limit: int = 100):
    """Get all categories from DB."""
    query = categories.select()
    return await database.fetch_all(query=query)

async def get_categories_by_name(filter: str, limit: int = 100):
    """Get all categories that match to specific filter from DB."""
    query = categories.query.filter(categories.name.contains(filter))
    print(query)
    return await database.fetch_all(query=query)
