"""add foriegn-key to posts table

Revision ID: f001ef2c6d63
Revises: e8fc6b084bed
Create Date: 2025-12-29 11:06:52.104699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f001ef2c6d63'
down_revision: Union[str, Sequence[str], None] = 'e8fc6b084bed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', 
    referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("post_users_fk", table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
