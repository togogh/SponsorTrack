"""reset

Revision ID: b9e577741f98
Revises:
Create Date: 2025-07-29 20:12:52.813901

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b9e577741f98"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "flag",
        sa.Column("entity_id", sa.UUID(), nullable=False),
        sa.Column(
            "entity_flagged",
            sa.Enum(
                "video",
                "sponsorship",
                "sponsored_segment",
                name="entitytype",
                schema="app",
                inherit_schema=True,
            ),
            nullable=False,
        ),
        sa.Column("field_flagged", sa.String(), nullable=False),
        sa.Column("value_flagged", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "resolved",
                "dismissed",
                name="flagstatus",
                schema="app",
                inherit_schema=True,
            ),
            nullable=True,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="app",
    )
    op.create_index(
        op.f("ix_app_flag_entity_flagged"), "flag", ["entity_flagged"], unique=False, schema="app"
    )
    op.create_index(
        op.f("ix_app_flag_entity_id"), "flag", ["entity_id"], unique=False, schema="app"
    )
    op.create_index(
        op.f("ix_app_flag_field_flagged"), "flag", ["field_flagged"], unique=False, schema="app"
    )
    op.create_index(op.f("ix_app_flag_id"), "flag", ["id"], unique=True, schema="app")
    op.create_index(op.f("ix_app_flag_status"), "flag", ["status"], unique=False, schema="app")
    op.create_table(
        "video",
        sa.Column("youtube_id", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("upload_date", sa.Date(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("duration", sa.Float(), nullable=True),
        sa.Column("channel", sa.String(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("youtube_id"),
        schema="app",
    )
    op.create_index(op.f("ix_app_video_id"), "video", ["id"], unique=True, schema="app")
    op.create_index(
        op.f("ix_app_video_language"), "video", ["language"], unique=False, schema="app"
    )
    op.create_table(
        "sponsoredsegment",
        sa.Column("sponsorblock_id", sa.String(), nullable=True),
        sa.Column("start_time", sa.Float(), nullable=False),
        sa.Column("end_time", sa.Float(), nullable=False),
        sa.Column("subtitles", sa.String(), nullable=True),
        sa.Column("parent_video_id", sa.UUID(), nullable=False),
        sa.Column(
            "time_range",
            postgresql.NUMRANGE(),
            sa.Computed("numrange(start_time::numeric, end_time::numeric)", persisted=True),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        postgresql.ExcludeConstraint(
            (sa.column("parent_video_id"), "="),
            (sa.column("time_range"), "&&"),
            using="gist",
            name="no_overlap_per_video",
        ),
        sa.ForeignKeyConstraint(
            ["parent_video_id"],
            ["app.video.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sponsorblock_id"),
        schema="app",
    )
    op.create_index(
        op.f("ix_app_sponsoredsegment_id"), "sponsoredsegment", ["id"], unique=True, schema="app"
    )
    op.create_index(
        op.f("ix_app_sponsoredsegment_parent_video_id"),
        "sponsoredsegment",
        ["parent_video_id"],
        unique=False,
        schema="app",
    )
    op.create_table(
        "videometadata",
        sa.Column("raw_json", sa.JSON(), nullable=False),
        sa.Column("raw_transcript", sa.JSON(), nullable=True),
        sa.Column("video_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["video_id"],
            ["app.video.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="app",
    )
    op.create_index(
        op.f("ix_app_videometadata_id"), "videometadata", ["id"], unique=True, schema="app"
    )
    op.create_index(
        op.f("ix_app_videometadata_video_id"),
        "videometadata",
        ["video_id"],
        unique=True,
        schema="app",
    )
    op.create_table(
        "sponsorship",
        sa.Column("sponsor_name", sa.String(), nullable=False),
        sa.Column("sponsor_description", sa.String(), nullable=True),
        sa.Column("sponsor_links", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("sponsor_coupon_code", sa.String(), nullable=True),
        sa.Column("sponsor_offer", sa.String(), nullable=True),
        sa.Column("sponsored_segment_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sponsored_segment_id"],
            ["app.sponsoredsegment.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="app",
    )
    op.create_index(op.f("ix_app_sponsorship_id"), "sponsorship", ["id"], unique=True, schema="app")
    op.create_index(
        op.f("ix_app_sponsorship_sponsored_segment_id"),
        "sponsorship",
        ["sponsored_segment_id"],
        unique=False,
        schema="app",
    )
    op.create_table(
        "generatedsponsorship",
        sa.Column("sponsor_name", sa.String(), nullable=False),
        sa.Column("sponsor_description", sa.String(), nullable=True),
        sa.Column("sponsor_links", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("sponsor_coupon_code", sa.String(), nullable=True),
        sa.Column("sponsor_offer", sa.String(), nullable=True),
        sa.Column("generator", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=True),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("prompt", sa.String(), nullable=True),
        sa.Column("sponsorship_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sponsorship_id"],
            ["app.sponsorship.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="app",
    )
    op.create_index(
        op.f("ix_app_generatedsponsorship_id"),
        "generatedsponsorship",
        ["id"],
        unique=True,
        schema="app",
    )
    op.create_index(
        op.f("ix_app_generatedsponsorship_sponsorship_id"),
        "generatedsponsorship",
        ["sponsorship_id"],
        unique=False,
        schema="app",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_app_generatedsponsorship_sponsorship_id"),
        table_name="generatedsponsorship",
        schema="app",
    )
    op.drop_index(
        op.f("ix_app_generatedsponsorship_id"), table_name="generatedsponsorship", schema="app"
    )
    op.drop_table("generatedsponsorship", schema="app")
    op.drop_index(
        op.f("ix_app_sponsorship_sponsored_segment_id"), table_name="sponsorship", schema="app"
    )
    op.drop_index(op.f("ix_app_sponsorship_id"), table_name="sponsorship", schema="app")
    op.drop_table("sponsorship", schema="app")
    op.drop_index(op.f("ix_app_videometadata_video_id"), table_name="videometadata", schema="app")
    op.drop_index(op.f("ix_app_videometadata_id"), table_name="videometadata", schema="app")
    op.drop_table("videometadata", schema="app")
    op.drop_index(
        op.f("ix_app_sponsoredsegment_parent_video_id"), table_name="sponsoredsegment", schema="app"
    )
    op.drop_index(op.f("ix_app_sponsoredsegment_id"), table_name="sponsoredsegment", schema="app")
    op.drop_table("sponsoredsegment", schema="app")
    op.drop_index(op.f("ix_app_video_language"), table_name="video", schema="app")
    op.drop_index(op.f("ix_app_video_id"), table_name="video", schema="app")
    op.drop_table("video", schema="app")
    op.drop_index(op.f("ix_app_flag_status"), table_name="flag", schema="app")
    op.drop_index(op.f("ix_app_flag_id"), table_name="flag", schema="app")
    op.drop_index(op.f("ix_app_flag_field_flagged"), table_name="flag", schema="app")
    op.drop_index(op.f("ix_app_flag_entity_id"), table_name="flag", schema="app")
    op.drop_index(op.f("ix_app_flag_entity_flagged"), table_name="flag", schema="app")
    op.drop_table("flag", schema="app")
    # ### end Alembic commands ###
