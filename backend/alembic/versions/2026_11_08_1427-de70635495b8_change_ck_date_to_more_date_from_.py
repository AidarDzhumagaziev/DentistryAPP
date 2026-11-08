"""change ck_date_to_more_date_from_schedule_exceptions to >=

Revision ID: de70635495b8
Revises: fec61980b67d
Create Date: 2026-11-08 14:27:46.018253

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "de70635495b8"
down_revision: Union[str, Sequence[str], None] = "fec61980b67d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        "ck_date_to_more_date_from_schedule_exceptions",
        "schedule_exceptions",
        type_="check",
    )
    op.create_check_constraint(
        "ck_date_to_more_date_from_schedule_exceptions",
        "schedule_exceptions",
        "date_to >= date_from",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_date_to_more_date_from_schedule_exceptions",
        "schedule_exceptions",
        type_="check",
    )
    op.create_check_constraint(
        "ck_date_to_more_date_from_schedule_exceptions",
        "schedule_exceptions",
        "date_to > date_from",
    )
