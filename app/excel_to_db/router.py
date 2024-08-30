import os

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.excel_to_db.dao import ExcelDAO
from app.excel_to_db.funcs import get_file, remove_file

router = APIRouter(prefix="/excel", tags=["Excel"])


@router.post("/upload")
async def upload(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
) -> None:
    filename = await get_file(file=file)

    await ExcelDAO.excel_to_db(filename, session=session)
    os.remove(filename)


@router.post("/users")
async def add_users(session: AsyncSession = Depends(get_session)) -> None:
    await ExcelDAO.add_users(session=session)


@router.post("/add_connection")
async def add_connection(
    file: UploadFile = File(...), session: AsyncSession = Depends(get_session)
) -> None:
    filename = await get_file(file=file)

    await ExcelDAO.add_connection(filename, session=session)
    os.remove(filename)


@router.post("/xlsx/")
async def download_accounts_xlsx(stats: list[dict], background_tasks: BackgroundTasks):
    try:
        file_path = "organizations.xlsx"
        await ExcelDAO.save_accounts_to_xlsx(stats=stats)
        background_tasks.add_task(remove_file, file_path)
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="organizations.xlsx",
        )
    except KeyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Данные статистики пустые"
        )
