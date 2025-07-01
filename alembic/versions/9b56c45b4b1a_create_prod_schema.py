"""create prod schema

Revision ID: 9b56c45b4b1a
Revises: 993626339da8
Create Date: 2025-07-01 10:09:47.106838

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b56c45b4b1a"
down_revision: Union[str, None] = "993626339da8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS prod")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SCHEMA IF EXISTS prod CASCADE")
