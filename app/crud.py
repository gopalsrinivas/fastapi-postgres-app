from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, desc
from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


async def create_item(db: AsyncSession, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_all_items(db: AsyncSession, skip: int = 0, limit: int = 10, is_active: bool = True):
    stmt = (
        select(Item)
        .filter(Item.is_active == is_active)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Item.created_at))
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_single_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    return result.scalars().first()


async def update_item(db: AsyncSession, item_id: int, item_update: ItemUpdate):
    stmt = (
        update(Item)
        .where(Item.id == item_id)
        .values(**item_update.dict(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()
    return await get_single_item(db, item_id)


async def delete_item(db: AsyncSession, item_id: int):
    stmt = delete(Item).where(Item.id == item_id)
    await db.execute(stmt)
    await db.commit()
