"""Include updated_at column for todos table

Revision ID: f48f5c6aadea
Revises: bc45a6f107b0
Create Date: 2026-10-21 18:20:59.405816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f48f5c6aadea'
down_revision: Union[str, Sequence[str], None] = 'bc45a6f107b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("todos",
          sa.Column(
              "updated_at",
              sa.DateTime(timezone=True),
                onupdate=sa.text("NOW()")
          )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("todos", "updated_at")
