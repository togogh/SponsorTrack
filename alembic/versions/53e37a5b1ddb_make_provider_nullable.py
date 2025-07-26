"""make provider nullable

Revision ID: 53e37a5b1ddb
Revises: 210ef4cadf9d
Create Date: 2025-07-18 21:32:16.192870

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "53e37a5b1ddb"
down_revision: Union[str, None] = "210ef4cadf9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "generatedsponsorship", "provider", existing_type=sa.String(), nullable=True, schema="dev"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        UPDATE dev.generatedsponsorship
        SET provider = ''
        WHERE provider IS NULL
    """)
    op.alter_column(
        "generatedsponsorship", "provider", existing_type=sa.String(), nullable=False, schema="dev"
    )
