from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=schemas.SuccessResponse, status_code=201)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        created_item = await crud.create_item(db, item)
        return schemas.SuccessResponse(
            message="Item created successfully",
            data=created_item,
            response_code=201
        )
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=schemas.SuccessResponse)
async def get_all_items(skip: int = 0, limit: int = 10, is_active: bool = True, db: AsyncSession = Depends(get_db)):
    try:
        items = await crud.get_all_items(db, skip=skip, limit=limit, is_active=is_active)
        return schemas.SuccessResponse(
            message="Items retrieved successfully",
            data=items,
            response_code=200
        )
    except Exception as e:
        logger.error(f"Error retrieving items: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{item_id}", response_model=schemas.SuccessResponse)
async def get_single_item(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        item = await crud.get_single_item(db, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return schemas.SuccessResponse(
            message="Item retrieved successfully",
            data=item,
            response_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving item with id {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{item_id}", response_model=schemas.SuccessResponse)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_item = await crud.update_item(db, item_id, item)
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return schemas.SuccessResponse(
            message="Item updated successfully",
            data=updated_item,
            response_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error updating item with id {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{item_id}", response_model=schemas.SuccessResponse)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        item = await crud.get_single_item(db, item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await crud.delete_item(db, item_id)
        return schemas.SuccessResponse(
            message="Item deleted successfully",
            data=item,
            response_code=200
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting item with id {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
