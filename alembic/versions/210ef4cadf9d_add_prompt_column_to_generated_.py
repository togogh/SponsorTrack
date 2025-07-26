"""add prompt column to generated sponsorship

Revision ID: 210ef4cadf9d
Revises: d2944d4cfb3b
Create Date: 2025-07-14 20:40:15.851615

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "210ef4cadf9d"
down_revision: Union[str, None] = "d2944d4cfb3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "generatedsponsorship", sa.Column("prompt", sa.String(), nullable=True), schema="dev"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("generatedsponsorship", "prompt", schema="dev")
