import pytest
from api.models import s4

def test_s4model_fields():
    model = s4.S4Model()
    # Check default values
    assert hasattr(model, "id")
    assert hasattr(model, "file_hash")
    assert hasattr(model, "compressed")
    assert hasattr(model, "created_at")
    assert hasattr(model, "updated_at")
    # Check default compressed value
    assert model.compressed is False

def test_s4symlink_fields():
    symlink = s4.S4Symlink()
    assert hasattr(symlink, "id")
    assert hasattr(symlink, "source_id")
    assert hasattr(symlink, "file_name")
    assert hasattr(symlink, "source")
    assert hasattr(symlink, "created_at")
    assert hasattr(symlink, "updated_at")

def test_s4model_tablename():
    assert s4.S4Model.__tablename__ == "s4_storage"

def test_s4symlink_tablename():
    assert s4.S4Symlink.__tablename__ == "s4_symlink"