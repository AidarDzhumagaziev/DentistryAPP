"""add default value in 'no_show_count' column in patients table

Revision ID: bf98c5f817cb
Revises: 4eab5132ab4b
Create Date: 2026-11-16 12:58:15.349720

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bf98c5f817cb"
down_revision: Union[str, Sequence[str], None] = "4eab5132ab4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("patients", "no_show_count", server_default="0")


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("patients", "no_show_count", server_default=None)
