import os
from api.services.s4_service import get_unlinked_files


def delete_unlinked_files():
    files = get_unlinked_files()
    map(lambda file: os.remove(file), files)


def garbage_collector():
    delete_unlinked_files()
