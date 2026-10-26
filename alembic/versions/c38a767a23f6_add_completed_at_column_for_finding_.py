"""Add completed_at column for finding duration

Revision ID: c38a767a23f6
Revises: 173ad7bb3f8d
Create Date: 2026-10-26 13:13:40.425558

"""
from typing import Sequence, Union
from xmlrpc.client import DateTime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c38a767a23f6'
down_revision: Union[str, Sequence[str], None] = '173ad7bb3f8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "todos",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True
        )
    )


def downgrade() -> None:
    op.drop_column("todos", "completed_at")
