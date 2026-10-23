"""Include created_at column for todos table

Revision ID: ad56386f3f01
Revises: 
Create Date: 2026-10-21 16:16:16.460591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad56386f3f01'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("todos", sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        server_default=sa.text("NOW()"),
        nullable=True
    ))
    op.execute(
        """
            UPDATE todos
            SET created_at = '2026-10-21 10:30:00+00'
            WHERE created_at IS NULL
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("todos", "created_at")
