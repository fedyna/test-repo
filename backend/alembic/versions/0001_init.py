"""init

Revision ID: 0001
Revises:
Create Date: 2026-03-24
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('channels',
        sa.Column('yt_channel_id', sa.String(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=False),
        sa.Column('language_guess', sa.String()),
        sa.Column('subscribers', sa.Integer()),
        sa.Column('total_views', sa.Integer()),
        sa.Column('video_count', sa.Integer()),
        sa.Column('relevance_score', sa.Float(), server_default='0'),
        sa.Column('status', sa.String(), server_default='active'),
        sa.Column('discovered_by', sa.String(), server_default='search'),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )
    op.create_table('videos',
        sa.Column('yt_video_id', sa.String(), primary_key=True),
        sa.Column('yt_channel_id', sa.String(), sa.ForeignKey('channels.yt_channel_id')),
        sa.Column('title', sa.String()),
        sa.Column('description', sa.Text()),
        sa.Column('published_at', sa.DateTime()),
        sa.Column('duration_seconds', sa.Integer()),
        sa.Column('is_short', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('tags', sa.JSON()),
        sa.Column('language_guess', sa.String()),
        sa.Column('cluster_id', sa.Integer()),
        sa.Column('status', sa.String(), server_default='active'),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )
    op.create_table('video_snapshots',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('yt_video_id', sa.String(), sa.ForeignKey('videos.yt_video_id')),
        sa.Column('captured_at', sa.DateTime()),
        sa.Column('view_count', sa.Integer()),
        sa.Column('like_count', sa.Integer()),
        sa.Column('comment_count', sa.Integer()),
    )
    op.create_table('video_scores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('yt_video_id', sa.String(), sa.ForeignKey('videos.yt_video_id')),
        sa.Column('window_hours', sa.Integer()),
        sa.Column('captured_at', sa.DateTime()),
        sa.Column('score_total', sa.Float()),
        sa.Column('views_velocity', sa.Float()),
        sa.Column('likes_velocity', sa.Float()),
        sa.Column('comments_velocity', sa.Float()),
        sa.Column('acceleration', sa.Float()),
        sa.Column('relative_views_z', sa.Float()),
        sa.Column('relative_engagement_z', sa.Float()),
        sa.Column('cluster_id', sa.Integer()),
        sa.Column('explanation_json', sa.JSON()),
    )
    op.create_table('clusters',
        sa.Column('cluster_id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), unique=True),
        sa.Column('seed_keywords', sa.JSON()),
        sa.Column('description', sa.Text()),
    )
    op.create_table('settings',
        sa.Column('key', sa.String(), primary_key=True),
        sa.Column('value', sa.JSON()),
    )


def downgrade() -> None:
    op.drop_table('settings')
    op.drop_table('clusters')
    op.drop_table('video_scores')
    op.drop_table('video_snapshots')
    op.drop_table('videos')
    op.drop_table('channels')
