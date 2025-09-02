"""create feature_flags table

Revision ID: 73e2dbe255a2
Revises: 
Create Date: 2025-09-01 19:40:15.133662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73e2dbe255a2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "feature_flags",
        sa.Column("key", sa.String(length=64), primary_key=True),
        sa.Column("enabled", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("feature_flags")
