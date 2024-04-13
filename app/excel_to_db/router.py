import os
from fastapi import UploadFile, File, APIRouter
from app.excel_to_db.dao import ExcelToDBDAO


router = APIRouter(prefix="/excel", tags=["Добавление excel в БД"])


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f"{file.filename}", "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    await ExcelToDBDAO.excel_to_db(file.filename)
    os.remove(file.filename)
