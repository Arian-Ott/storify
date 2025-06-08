from fastapi import HTTPException
import lzma
from hashlib import sha3_256
from api.models.s4 import S4Model, S4Symlink
import os
import uuid
from api.db import get_db
from fastapi.responses import StreamingResponse
from io import BytesIO

S4_STORAGE_LOCATION = os.getenv("S4_STORAGE_LOCATION", "s4")


def create_file(
    file_name: str, user_id,file_bytes: bytes, file_type: str = "application/octet-stream"
):
    file_id = uuid.uuid4()
    file_hash = sha3_256(file_bytes).hexdigest()
    with next(get_db()) as db:
        existing_file = db.query(S4Model).filter(S4Model.file_hash == file_hash).first()

        if not existing_file:
            obj = S4Model(
                id=file_id,
                file_hash=file_hash,
            )
            db.add(obj)
            db.commit()
            db.refresh(obj)
            compressed_bytes = lzma.compress(file_bytes)

            with open("s4/" + str(file_id) + ".xz", "wb") as f:
                f.write(compressed_bytes)

        symlink = S4Symlink(
            id=file_id,
            source_id=file_id if not existing_file else existing_file.id,
            file_name=file_name,
            user_id=uuid.UUID(user_id),
        )
        db.add(symlink)
        db.commit()

    # Compress the file using lzma (XZ format)

    return {
        "id": str(file_id),
        "file_name": file_name,
        "file_type": file_type,
        "message": "File created and compressed successfully",
    }


def get_file(file_id: str):
    file_id = uuid.UUID(file_id)
    with next(get_db()) as db:
        symlink = db.query(S4Symlink).filter(S4Symlink.id == file_id).first()
        if not symlink:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = os.path.join(S4_STORAGE_LOCATION, f"{symlink.source_id}.xz")
        print(file_path)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found in storage")

        try:
            with open(file_path, "rb") as f:
                compressed_bytes = f.read()
                file_bytes = lzma.decompress(compressed_bytes)
        except (lzma.LZMAError, OSError):
            raise HTTPException(status_code=500, detail="Failed to decompress file")

    return StreamingResponse(
        content=BytesIO(file_bytes),
        headers={"Content-Disposition": f'inline; filename="{symlink.file_name}"'},
    )


def get_unlinked_files():
    unlinked_files = []
    with next(get_db()) as db:
        symlinks = db.query(S4Model.id).all()
    for symlink in symlinks:
        if not os.path.exists(os.path.join(S4_STORAGE_LOCATION, f"{symlink.id}.xz")):
            unlinked_files.append(symlink.id)

    return unlinked_files


def delete_unlinked_files(unlinked_files):
    with next(get_db()) as db:
        for file_id in unlinked_files:
            file = db.query(S4Model).filter(S4Model.id == file_id).first()
            if file:
                db.delete(file)
                db.commit()
            file_path = os.path.join(S4_STORAGE_LOCATION, f"{file_id}.xz")
            if os.path.exists(file_path):
                os.remove(file_path)


def get_all_files():
    with next(get_db()) as db:
        symlinks = db.query(S4Symlink).all()
    return [
        {
            "id": str(symlink.id),
            "file_name": symlink.file_name,
            "created_at": symlink.created_at,
            "updated_at": symlink.updated_at,
        }
        for symlink in symlinks
    ]
    
def get_symlinks_by_user(user_id: str):
    user_id = uuid.UUID(user_id)
    with next(get_db()) as db:
        symlinks = db.query(S4Symlink).filter(S4Symlink.user_id == user_id).all()
    return [
        {
            "id": str(symlink.id),
            "file_name": symlink.file_name,
            "created_at": symlink.created_at,
            "updated_at": symlink.updated_at,
        }
        for symlink in symlinks
    ]