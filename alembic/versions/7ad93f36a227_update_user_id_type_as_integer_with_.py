"""Update user_id type as integer with foreign key constraints

Revision ID: 7ad93f36a227
Revises: f701f6b4d5ed
Create Date: 2026-11-03 16:43:07.035438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ad93f36a227'
down_revision: Union[str, Sequence[str], None] = 'f701f6b4d5ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "user_memories",
        "user_id",
        existing_type=sa.String(length=50),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using='user_id::integer'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "user_memories",
        "user_id",
        existing_type=sa.Integer(),
        type_=sa.String(length=50),
        existing_nullable=False,
        postgresql_using='user_id::string'
    )
