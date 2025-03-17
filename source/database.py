from contextlib import asynccontextmanager
from source.settings import tortoise_orm
from tortoise import Tortoise


@asynccontextmanager
async def init():
    try:
        await Tortoise.init(config=tortoise_orm)
        await Tortoise.generate_schemas(safe=True)
        yield
    finally:
        await Tortoise.close_connections()