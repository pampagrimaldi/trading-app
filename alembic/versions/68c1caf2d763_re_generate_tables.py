"""re-generate tables

Revision ID: 68c1caf2d763
Revises: 
Create Date: 2023-12-04 13:07:51.639458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68c1caf2d763'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('symbol')
    )
    op.create_index(op.f('ix_stock_id'), 'stock', ['id'], unique=False)
    op.create_table('stock_price',
    sa.Column('stock_id', sa.Integer(), nullable=False),
    sa.Column('dt', sa.DateTime(), nullable=False),
    sa.Column('close', sa.Numeric(precision=10, scale=4), nullable=False),
    sa.Column('high', sa.Numeric(precision=10, scale=4), nullable=False),
    sa.Column('low', sa.Numeric(precision=10, scale=4), nullable=False),
    sa.Column('trade_count', sa.Integer(), nullable=False),
    sa.Column('open', sa.Numeric(precision=10, scale=4), nullable=False),
    sa.Column('volume', sa.Numeric(), nullable=False),
    sa.Column('vwap', sa.Numeric(precision=10, scale=4), nullable=False),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('stock_id', 'dt')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_price')
    op.drop_index(op.f('ix_stock_id'), table_name='stock')
    op.drop_table('stock')
    # ### end Alembic commands ###
