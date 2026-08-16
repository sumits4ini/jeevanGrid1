"""0001_initial_postgis_schema

Revision ID: 0001_initial_postgis
Revises: 
Create Date: 2026-08-16 21:30:00.000000 UTC

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '0001_initial_postgis'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable PostGIS Spatial Extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. Create disasters table
    op.create_table(
        'disasters',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('disaster_type', sa.String(length=50), nullable=False),
        sa.Column('severity_level', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('affected_population_estimate', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_disasters_id'), 'disasters', ['id'], unique=False)
    op.create_index(op.f('ix_disasters_name'), 'disasters', ['name'], unique=False)
    op.create_index(op.f('ix_disasters_disaster_type'), 'disasters', ['disaster_type'], unique=False)
    op.create_index(op.f('ix_disasters_status'), 'disasters', ['status'], unique=False)

    # 3. Create critical_infrastructure table
    op.create_table(
        'critical_infrastructure',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('facility_type', sa.String(length=50), nullable=False),
        sa.Column('operational_status', sa.String(length=50), nullable=False, server_default='OPERATIONAL'),
        sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('max_capacity', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('current_occupancy', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('backup_power_hours', sa.Float(), nullable=False, server_default='24.0'),
        sa.Column('contact_phone', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_critical_infrastructure_id'), 'critical_infrastructure', ['id'], unique=False)
    op.create_index(op.f('ix_critical_infrastructure_name'), 'critical_infrastructure', ['name'], unique=False)
    op.create_index(op.f('ix_critical_infrastructure_facility_type'), 'critical_infrastructure', ['facility_type'], unique=False)
    op.create_index(op.f('ix_critical_infrastructure_operational_status'), 'critical_infrastructure', ['operational_status'], unique=False)

    # 4. Create response_units table
    op.create_table(
        'response_units',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('unit_code', sa.String(length=50), nullable=False),
        sa.Column('unit_type', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='AVAILABLE'),
        sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('capacity_payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('assigned_incident_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_response_units_id'), 'response_units', ['id'], unique=False)
    op.create_index(op.f('ix_response_units_unit_code'), 'response_units', ['unit_code'], unique=True)
    op.create_index(op.f('ix_response_units_unit_type'), 'response_units', ['unit_type'], unique=False)
    op.create_index(op.f('ix_response_units_status'), 'response_units', ['status'], unique=False)
    op.create_index(op.f('ix_response_units_assigned_incident_id'), 'response_units', ['assigned_incident_id'], unique=False)

    # 5. Create hazard_zones table
    op.create_table(
        'hazard_zones',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('disaster_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=True),
        sa.Column('polygon_geom', geoalchemy2.types.Geometry(geometry_type='MULTIPOLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=False),
        sa.Column('inundation_depth_m', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('hazard_intensity', sa.Float(), nullable=False, server_default='0.5'),
        sa.Column('risk_level', sa.String(length=50), nullable=False, server_default='MODERATE'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['disaster_id'], ['disasters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hazard_zones_id'), 'hazard_zones', ['id'], unique=False)
    op.create_index(op.f('ix_hazard_zones_disaster_id'), 'hazard_zones', ['disaster_id'], unique=False)
    op.create_index(op.f('ix_hazard_zones_risk_level'), 'hazard_zones', ['risk_level'], unique=False)
    op.create_index(op.f('ix_hazard_zones_is_active'), 'hazard_zones', ['is_active'], unique=False)


def downgrade() -> None:
    op.drop_table('hazard_zones')
    op.drop_table('response_units')
    op.drop_table('critical_infrastructure')
    op.drop_table('disasters')
    # Note: We do not drop the postgis extension on downgrade to avoid impacting other schemas
