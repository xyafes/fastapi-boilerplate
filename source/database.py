from contextlib import asynccontextmanager
from source.settings import tortoise_orm
from tortoise import Tortoise


@asynccontextmanager
async def init():
    """Initialize the database connection."""
    try:
        await Tortoise.init(config=tortoise_orm)
        # safe=True, will just log warnings instead of erroring out if tables already exist
        await Tortoise.generate_schemas(safe=True)
        # Yield the connection
        yield
    finally:
        # Close the connection, when the context manager is done
        await Tortoise.close_connections()
