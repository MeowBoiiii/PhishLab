"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-01-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Identyfikator tej migracji oraz brak migracji poprzedzającej (to jest pierwsza migracja)
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Tworzy początkowy schemat 6 tabel, jeśli jeszcze nie istnieją w bazie."""
    # Pobranie listy istniejących tabel (zabezpiecza przed błędem, jeśli Docker wcześniej wykonał schema.sql)
    bind = op.get_bind()
    existing_tables = set(sa.inspect(bind).get_table_names())

    # 1. Tabela administratorów
    if "admins" not in existing_tables:
        op.create_table(
            "admins",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("username", sa.String(50), unique=True, nullable=False),
            sa.Column("email", sa.String(100), unique=True, nullable=False),
            sa.Column("password_hash", sa.String(255), nullable=False),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        )

    # 2. Tabela zanonimizowanych odbiorców kampanii
    if "target_users" not in existing_tables:
        op.create_table(
            "target_users",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("user_hash", sa.String(64), unique=True, nullable=False),
            sa.Column("department", sa.String(100), nullable=False),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
        )
        op.create_index("idx_target_users_department", "target_users", ["department"])

    # 3. Tabela szablonów maili i treści edukacyjnych
    if "templates" not in existing_tables:
        op.create_table(
            "templates",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(100), nullable=False),
            sa.Column("email_subject", sa.String(200), nullable=False),
            sa.Column("email_body", sa.Text(), nullable=False),
            sa.Column("edu_page_content", sa.Text(), nullable=False),
        )

    # 4. Tabela kampanii phishingowych
    if "campaigns" not in existing_tables:
        op.create_table(
            "campaigns",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(100), nullable=False),
            sa.Column("admin_id", sa.Integer(), sa.ForeignKey("admins.id", ondelete="SET NULL"), nullable=True),
            sa.Column("template_id", sa.Integer(), sa.ForeignKey("templates.id", ondelete="CASCADE"), nullable=False),
            sa.Column("target_department", sa.String(100), nullable=False),
            sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
            sa.Column("scheduled_at", sa.TIMESTAMP(), nullable=True),
            sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.func.now()),
            sa.CheckConstraint("status IN ('DRAFT', 'ACTIVE', 'FINISHED')", name="ck_campaigns_status"),
        )
        op.create_index("idx_campaigns_status", "campaigns", ["status"])

    # 5. Tabela śledzenia reakcji użytkowników (otwarcia, kliknięcia, quiz)
    if "campaign_tracking" not in existing_tables:
        op.create_table(
            "campaign_tracking",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("campaign_id", sa.Integer(), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("target_users.id", ondelete="CASCADE"), nullable=False),
            sa.Column("tracking_token", sa.String(64), unique=True, nullable=False),
            sa.Column("is_opened", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("is_clicked", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("reaction_time_sec", sa.Integer(), nullable=True),
            sa.Column("quiz_score", sa.Integer(), nullable=True),
            sa.UniqueConstraint("campaign_id", "user_id", name="uq_campaign_tracking_campaign_user"),
        )
        op.create_index("idx_campaign_tracking_campaign_id", "campaign_tracking", ["campaign_id"])
        op.create_index("idx_campaign_tracking_user_id", "campaign_tracking", ["user_id"])

    # 6. Tabela pytań do quizów edukacyjnych
    if "quiz_questions" not in existing_tables:
        op.create_table(
            "quiz_questions",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("template_id", sa.Integer(), sa.ForeignKey("templates.id", ondelete="CASCADE"), nullable=False),
            sa.Column("question", sa.String(255), nullable=False),
            sa.Column("option_a", sa.String(150), nullable=False),
            sa.Column("option_b", sa.String(150), nullable=False),
            sa.Column("option_c", sa.String(150), nullable=False),
            sa.Column("correct_answer", sa.CHAR(1), nullable=False),
            sa.CheckConstraint("correct_answer IN ('A', 'B', 'C')", name="ck_quiz_correct_answer"),
        )


def downgrade() -> None:
    """Cofa migrację - usuwa tabele w odwrotnej kolejności (ze względu na klucze obce)."""
    op.drop_table("quiz_questions")
    op.drop_table("campaign_tracking")
    op.drop_table("campaigns")
    op.drop_table("templates")
    op.drop_table("target_users")
    op.drop_table("admins")