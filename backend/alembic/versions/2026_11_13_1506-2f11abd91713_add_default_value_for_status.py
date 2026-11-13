"""add default value for status

Revision ID: 2f11abd91713
Revises: 89cf1a5f600a
Create Date: 2026-11-13 15:06:40.033804

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2f11abd91713"
down_revision: Union[str, Sequence[str], None] = "89cf1a5f600a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "appointments",
        "status",
        server_default=sa.text("'scheduled'"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "appointments",
        "status",
        server_default=None,
    )
