import os
import secrets
import string

from fastapi import File
from app.excel_to_db.types import Filename


async def remove_file(path: str) -> None:
    os.unlink(path)


async def get_file(file: File) -> Filename:
    try:
        contents = file.file.read()
        with open(f"{file.filename}", "wb") as f:
            f.write(contents)

        return file.filename
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()


async def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(16))

    return password
