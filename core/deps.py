from typing import Generator

from core.databes import Session


async def get_db() -> Generator:
    async with Session() as session:
        try:
            yield session
        finally:
            session.close()
