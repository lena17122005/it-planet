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
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('display_name', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('seeker', 'employer', 'curator', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'], unique=False)

    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('inn', sa.String(length=12), nullable=False),
        sa.Column('corporate_email', sa.String(length=255), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('owner_id'),
        sa.UniqueConstraint('corporate_email'),
    )
    op.create_index('ix_companies_name', 'companies', ['name'], unique=False)
    op.create_index('ix_companies_inn', 'companies', ['inn'], unique=False)

    op.create_table(
        'vacancies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('company_id', sa.Integer(), sa.ForeignKey('companies.id'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('salary_from', sa.Integer(), nullable=True),
        sa.Column('salary_to', sa.Integer(), nullable=True),
        sa.Column('type', sa.Enum('vacancy', 'internship', 'mentorship', 'event', name='vacancytype'), nullable=False),
        sa.Column('format', sa.Enum('office', 'hybrid', 'remote', name='workformat'), nullable=False),
        sa.Column('expires_at', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('ix_vacancies_title', 'vacancies', ['title'], unique=False)
    op.create_index('ix_vacancies_city', 'vacancies', ['city'], unique=False)
    op.create_index('ix_vacancies_company_id', 'vacancies', ['company_id'], unique=False)
    op.create_index('ix_vacancies_type', 'vacancies', ['type'], unique=False)
    op.create_index('ix_vacancies_format', 'vacancies', ['format'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_vacancies_format', table_name='vacancies')
    op.drop_index('ix_vacancies_type', table_name='vacancies')
    op.drop_index('ix_vacancies_company_id', table_name='vacancies')
    op.drop_index('ix_vacancies_city', table_name='vacancies')
    op.drop_index('ix_vacancies_title', table_name='vacancies')
    op.drop_table('vacancies')

    op.drop_index('ix_companies_inn', table_name='companies')
    op.drop_index('ix_companies_name', table_name='companies')
    op.drop_table('companies')

    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

    op.execute('DROP TYPE IF EXISTS workformat')
    op.execute('DROP TYPE IF EXISTS vacancytype')
    op.execute('DROP TYPE IF EXISTS userrole')
