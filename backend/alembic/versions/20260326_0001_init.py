"""initial schema

Revision ID: 20260326_0001
Revises:
Create Date: 2026-03-26
"""

from alembic import op
import sqlalchemy as sa

revision = '20260326_0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('seeker', 'employer', 'curator', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('is_blocked', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('email_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('full_name', sa.String(180), nullable=True),
        sa.Column('university', sa.String(180), nullable=True),
        sa.Column('graduation_year', sa.Integer(), nullable=True),
        sa.Column('about', sa.Text(), nullable=True),
        sa.Column('skills', sa.Text(), nullable=True),
        sa.Column('github_url', sa.String(255), nullable=True),
        sa.Column('portfolio_url', sa.String(255), nullable=True),
        sa.Column('profile_visibility', sa.Enum('all', 'contacts', 'nobody', name='profilevisibility'), server_default='all', nullable=False),
        sa.Column('show_responses', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('allow_contact_requests', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])

    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('inn', sa.String(12), nullable=False),
        sa.Column('corporate_email', sa.String(255), nullable=False),
        sa.Column('domain', sa.String(255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sphere', sa.String(120), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('social_links', sa.Text(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('verification_method', sa.String(50), nullable=True),
        sa.Column('verification_comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('owner_id'),
        sa.UniqueConstraint('corporate_email'),
    )

    op.create_table(
        'vacancies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('address', sa.String(255), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('salary_from', sa.Integer(), nullable=True),
        sa.Column('salary_to', sa.Integer(), nullable=True),
        sa.Column('type', sa.Enum('vacancy', 'internship', 'mentorship', 'event', name='vacancytype'), nullable=False),
        sa.Column('format', sa.Enum('office', 'hybrid', 'remote', name='workformat'), nullable=False),
        sa.Column('event_date', sa.Date(), nullable=True),
        sa.Column('expires_at', sa.Date(), nullable=True),
        sa.Column('tags_csv', sa.Text(), server_default='', nullable=False),
        sa.Column('is_closed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('moderation_status', sa.Enum('pending', 'published', 'rejected', name='moderationstatus'), server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'vacancy_responses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('vacancy_id', sa.Integer(), sa.ForeignKey('vacancies.id'), nullable=False),
        sa.Column('seeker_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.Enum('accepted', 'rejected', 'reserve', 'pending', name='responsestatus'), server_default='pending', nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('vacancy_id', 'seeker_id', name='uq_vacancy_response'),
    )

    op.create_table(
        'contact_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('requester_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('receiver_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'accepted', 'rejected', name='contactrequeststatus'), server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('requester_id', 'receiver_id', name='uq_contact_pair'),
    )

    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('ix_tags_name', 'tags', ['name'], unique=True)

    op.create_table(
        'moderation_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('curator_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('entity', sa.Enum('company', 'vacancy', 'tag', 'user', name='moderationentity'), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.Enum('approve', 'reject', 'edit', name='moderationaction'), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('moderation_logs')
    op.drop_index('ix_tags_name', table_name='tags')
    op.drop_table('tags')
    op.drop_table('contact_requests')
    op.drop_table('vacancy_responses')
    op.drop_table('vacancies')
    op.drop_table('companies')
    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
