from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .. import db
from .. import models
from .. import schemas

router = APIRouter(prefix="/api")


@router.post("/scientists", response_model=schemas.ScientistRead)
async def create_scientist(
    payload: schemas.ScientistCreate, session: AsyncSession = Depends(db.get_session)
):
    s = models.Scientist(**payload.dict())
    session.add(s)
    await session.commit()
    await session.refresh(s)
    return s


@router.get("/scientists", response_model=List[schemas.ScientistRead])
async def list_scientists(
    q: Optional[str] = Query(None),
    limit: int = 100,
    session: AsyncSession = Depends(db.get_session),
):
    stmt = models.Study = None
    # simple list for now
    result = await session.execute(models.Scientist.__table__.select().limit(limit))
    rows = result.fetchall()
    return [models.Scientist(**dict(row)) for row in rows]


@router.get("/scientists/{scientist_id}", response_model=schemas.ScientistRead)
async def get_scientist(
    scientist_id: int, session: AsyncSession = Depends(db.get_session)
):
    result = await session.get(models.Scientist, scientist_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/scientists/{scientist_id}", response_model=schemas.ScientistRead)
async def update_scientist(
    scientist_id: int,
    payload: schemas.ScientistCreate,
    session: AsyncSession = Depends(db.get_session),
):
    obj = await session.get(models.Scientist, scientist_id)
    if not obj:
        raise HTTPException(status_code=404)
    for k, v in payload.dict().items():
        setattr(obj, k, v)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete("/scientists/{scientist_id}", status_code=204)
async def delete_scientist(
    scientist_id: int, session: AsyncSession = Depends(db.get_session)
):
    obj = await session.get(models.Scientist, scientist_id)
    if not obj:
        raise HTTPException(status_code=404)
    await session.delete(obj)
    await session.commit()
    return None
