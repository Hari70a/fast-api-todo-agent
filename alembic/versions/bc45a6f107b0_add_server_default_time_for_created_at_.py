"""Add server default time for created at column

Revision ID: bc45a6f107b0
Revises: ad56386f3f01
Create Date: 2026-10-21 17:45:51.181661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc45a6f107b0'
down_revision: Union[str, Sequence[str], None] = 'ad56386f3f01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "todos",
        "created_at",
        server_default=sa.text("NOW()")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "todos",
        "created_at",
        server_default=None
    )

