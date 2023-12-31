"""add backtest components

Revision ID: 9548dce86c28
Revises: ad6067d3fe32
Create Date: 2023-12-17 11:03:28.614465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9548dce86c28'
down_revision: Union[str, None] = 'ad6067d3fe32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('backtest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_strategy_stock_id', sa.Integer(), nullable=True),
    sa.Column('stock_strategy_strategy_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['stock_strategy_stock_id', 'stock_strategy_strategy_id'], ['stock_strategy.stock_id', 'stock_strategy.strategy_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_id'), 'backtest', ['id'], unique=False)
    op.create_table('backtest_charts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('backtest_id', sa.Integer(), nullable=True),
    sa.Column('chart_data', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_charts_id'), 'backtest_charts', ['id'], unique=False)
    op.create_table('backtest_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('backtest_id', sa.Integer(), nullable=True),
    sa.Column('order_data', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_orders_id'), 'backtest_orders', ['id'], unique=False)
    op.create_table('backtest_profit_loss',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('backtest_id', sa.Integer(), nullable=True),
    sa.Column('profit_loss_data', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_profit_loss_id'), 'backtest_profit_loss', ['id'], unique=False)
    op.create_table('backtest_statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('backtest_id', sa.Integer(), nullable=True),
    sa.Column('statistic_name', sa.String(), nullable=False),
    sa.Column('statistic_value', sa.Numeric(), nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtest_statistics_id'), 'backtest_statistics', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_backtest_statistics_id'), table_name='backtest_statistics')
    op.drop_table('backtest_statistics')
    op.drop_index(op.f('ix_backtest_profit_loss_id'), table_name='backtest_profit_loss')
    op.drop_table('backtest_profit_loss')
    op.drop_index(op.f('ix_backtest_orders_id'), table_name='backtest_orders')
    op.drop_table('backtest_orders')
    op.drop_index(op.f('ix_backtest_charts_id'), table_name='backtest_charts')
    op.drop_table('backtest_charts')
    op.drop_index(op.f('ix_backtest_id'), table_name='backtest')
    op.drop_table('backtest')
    # ### end Alembic commands ###
