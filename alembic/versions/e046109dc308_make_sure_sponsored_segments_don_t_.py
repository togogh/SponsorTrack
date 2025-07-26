"""make sure sponsored segments don't overlap

Revision ID: e046109dc308
Revises: 1ef882c91f7b
Create Date: 2025-07-11 20:07:02.842890

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "e046109dc308"
down_revision: Union[str, None] = "1ef882c91f7b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.add_column(
        "sponsoredsegment",
        sa.Column(
            "time_range",
            postgresql.NUMRANGE(),
            sa.Computed("numrange(start_time::numeric, end_time::numeric)", persisted=True),
            nullable=False,
        ),
        schema="dev",
    )
    op.create_exclude_constraint(
        "no_overlap_per_video",
        "sponsoredsegment",
        ("time_range", "&&"),
        ("parent_video_id", "="),
        using="gist",
        schema="dev",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("no_overlap_per_video", "sponsoredsegment", type_="exclude", schema="dev")
    op.drop_column("sponsoredsegment", "time_range", schema="dev")
