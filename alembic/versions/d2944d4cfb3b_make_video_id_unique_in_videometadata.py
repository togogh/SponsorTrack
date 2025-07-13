"""make video_id unique in videometadata

Revision ID: d2944d4cfb3b
Revises: e046109dc308
Create Date: 2025-07-13 16:35:01.119686

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d2944d4cfb3b"
down_revision: Union[str, None] = "e046109dc308"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "videometadata_video_id_key", "videometadata", ["video_id"], schema="dev"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("videometadata_video_id_key", "videometadata", schema="dev")
