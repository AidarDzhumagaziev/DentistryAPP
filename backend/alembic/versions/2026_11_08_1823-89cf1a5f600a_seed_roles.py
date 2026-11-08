"""seed roles

Revision ID: 89cf1a5f600a
Revises: de70635495b8
Create Date: 2026-11-08 18:23:09.865073

"""

from typing import Sequence, Union

from common.enums.enums_db import RoleType

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "89cf1a5f600a"
down_revision: Union[str, Sequence[str], None] = "de70635495b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    roles_table = sa.table("roles", sa.column("name", sa.String))
    op.bulk_insert(
        roles_table,
        [
            {
                "name": RoleType.ADMIN.value,
            },
            {
                "name": RoleType.PATIENT.value,
            },
            {
                "name": RoleType.DOCTOR.value,
            },
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM roles WHERE name IN ('PATIENT', 'DOCTOR', 'ADMIN')")
