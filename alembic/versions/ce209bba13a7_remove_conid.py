"""remove conid

Revision ID: ce209bba13a7
Revises: b2e79dc87c53
Create Date: 2023-12-06 23:48:21.443732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce209bba13a7'
down_revision: Union[str, None] = 'b2e79dc87c53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('stock_conid_key', 'stock', type_='unique')
    op.drop_column('stock', 'conid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('conid', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('stock_conid_key', 'stock', ['conid'])
    # ### end Alembic commands ###
