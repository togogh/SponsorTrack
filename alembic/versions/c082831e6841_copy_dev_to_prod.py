"""copy dev to prod

Revision ID: c082831e6841
Revises: 1620f43714c8
Create Date: 2025-07-01 17:03:30.004844

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = "c082831e6841"
down_revision: Union[str, None] = "1620f43714c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = [
        "video",
        "videometadata",
        "sponsoredsegment",
        "sponsorship",
        "generatedsponsorship",
        "flag",
    ]
    for table in tables:
        if table == "flag":
            op.execute("""
                INSERT INTO prod.flag (
                    id, created_at, updated_at, entity_id, entity_flagged, field_flagged, value_flagged, status
                )
                SELECT
                    id,
                    created_at,
                    updated_at,
                    entity_id,
                    entity_flagged::text::prod.entitytype,
                    field_flagged,
                    value_flagged,
                    status::text::prod.flagstatus    
                FROM dev.flag       
            """)
        else:
            dev_columns = inspector.get_columns(table, schema="dev")
            column_names = [col["name"] for col in dev_columns]
            columns_sql = ", ".join(column_names)
            insert_sql = f"""
                INSERT INTO prod.{table} ({columns_sql})
                SELECT {columns_sql}
                FROM dev.{table};
            """
            op.execute(insert_sql)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names(schema="dev")
    for table in tables:
        op.execute(f"TRUNCATE TABLE prod.{table} CASCADE;")
