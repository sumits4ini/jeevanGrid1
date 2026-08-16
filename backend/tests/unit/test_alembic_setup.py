"""
Unit Tests for Alembic Migration Configuration and Metadata
"""

from pathlib import Path
from alembic.config import Config
from alembic.script import ScriptDirectory
from backend.app.db.base import Base


def test_alembic_config_and_script_directory():
    """Verifies that alembic.ini points to a valid script directory and migrations."""
    root_path = Path(__file__).resolve().parents[3]
    alembic_ini_path = root_path / "alembic.ini"
    assert alembic_ini_path.exists(), f"alembic.ini must exist at repository root ({alembic_ini_path})"

    alembic_cfg = Config(str(alembic_ini_path))
    script = ScriptDirectory.from_config(alembic_cfg)
    heads = script.get_heads()

    assert len(heads) == 1, "There should be exactly one migration head"
    assert heads[0] == "0001_initial_postgis"


def test_registered_metadata_tables():
    """Verifies that all core tables are registered in Base.metadata for migrations."""
    table_names = set(Base.metadata.tables.keys())
    expected_tables = {
        "disasters",
        "critical_infrastructure",
        "response_units",
        "hazard_zones",
    }
    assert expected_tables.issubset(table_names), f"Missing tables in metadata: {expected_tables - table_names}"
