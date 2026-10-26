"""Make updated_at column as currenttime when created

Revision ID: d5720feb2cea
Revises: c38a767a23f6
Create Date: 2026-10-26 13:58:17.230600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5720feb2cea'
down_revision: Union[str, Sequence[str], None] = 'c38a767a23f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "todos",
        "updated_at",
        server_default=sa.text("NOW()"),
    )


def downgrade() -> None:
    op.alter_column(
        "todos",
        "updated_at",
        server_default=None
    )
