"""delete stock_price_table

Revision ID: bd5537de5424
Revises: 0d073ec735f6
Create Date: 2023-12-02 19:45:41.506706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd5537de5424'
down_revision: Union[str, None] = '0d073ec735f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_stock_price_id', table_name='stock_price')
    op.drop_table('stock_price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_price',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('stock_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('open', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('high', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('low', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('close', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('volume', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('vwap', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('trade_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], name='stock_price_stock_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='stock_price_pkey')
    )
    op.create_index('ix_stock_price_id', 'stock_price', ['id'], unique=False)
    # ### end Alembic commands ###