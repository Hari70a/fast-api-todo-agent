"""Make nullable as False for updated_at column for todos table

Revision ID: 173ad7bb3f8d
Revises: f48f5c6aadea
Create Date: 2026-10-21 18:28:45.516650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '173ad7bb3f8d'
down_revision: Union[str, Sequence[str], None] = 'f48f5c6aadea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
    """
        UPDATE todos
        SET updated_at = NOW()
        WHERE updated_at IS NULL
    """)
    op.alter_column(
        "todos",
        "updated_at",
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "todos",
        "updated_at",
        nullable=True
    )
