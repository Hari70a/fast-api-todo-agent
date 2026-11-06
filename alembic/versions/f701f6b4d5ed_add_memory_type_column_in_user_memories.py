"""Add memory type column in user memories

Revision ID: f701f6b4d5ed
Revises: 2e262945014a
Create Date: 2026-11-03 14:44:53.776153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f701f6b4d5ed'
down_revision: Union[str, Sequence[str], None] = '2e262945014a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add as nullable
    op.add_column(
        "user_memories",
        sa.Column(
            "memory_type",
            sa.String(length=50),
            nullable=True
        )
    )

    # 2. Give existing records a value
    op.execute(
        """
        UPDATE user_memories
        SET memory_type = 'semantic'
        WHERE memory_type IS NULL
        """
    )

    # 3: Alter column with memory_type not null
    op.alter_column(
        "user_memories",
        "memory_type",
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_memories", "memory_type")
