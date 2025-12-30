"""add content columns to post table

Revision ID: 34426cdf1cc8
Revises: 35a35677d10e
Create Date: 2025-12-28 13:03:56.775069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34426cdf1cc8'
down_revision: Union[str, Sequence[str], None] = '35a35677d10e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content'), sa.String(), nullable=False)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
