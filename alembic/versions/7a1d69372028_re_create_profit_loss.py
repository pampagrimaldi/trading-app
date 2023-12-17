"""re-create profit-loss

Revision ID: 7a1d69372028
Revises: a1e16cc4c826
Create Date: 2023-12-17 17:50:34.158250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a1d69372028'
down_revision: Union[str, None] = 'a1e16cc4c826'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    sa.Column('total_trades', sa.Integer(), nullable=True),
    sa.Column('average_win', sa.Numeric(), nullable=True),
    sa.Column('average_loss', sa.Numeric(), nullable=True),
    sa.Column('compounding_annual_return', sa.Numeric(), nullable=True),
    sa.Column('drawdown', sa.Numeric(), nullable=True),
    sa.Column('expectancy', sa.Numeric(), nullable=True),
    sa.Column('net_profit', sa.Numeric(), nullable=True),
    sa.Column('sharpe_ratio', sa.Numeric(), nullable=True),
    sa.Column('sortino_ratio', sa.Numeric(), nullable=True),
    sa.Column('probabilistic_sharpe_ratio', sa.Numeric(), nullable=True),
    sa.Column('loss_rate', sa.Numeric(), nullable=True),
    sa.Column('win_rate', sa.Numeric(), nullable=True),
    sa.Column('profit_loss_ratio', sa.Numeric(), nullable=True),
    sa.Column('alpha', sa.Numeric(), nullable=True),
    sa.Column('beta', sa.Numeric(), nullable=True),
    sa.Column('annual_standard_deviation', sa.Numeric(), nullable=True),
    sa.Column('annual_variance', sa.Numeric(), nullable=True),
    sa.Column('information_ratio', sa.Numeric(), nullable=True),
    sa.Column('tracking_error', sa.Numeric(), nullable=True),
    sa.Column('treynor_ratio', sa.Numeric(), nullable=True),
    sa.Column('total_fees', sa.Numeric(), nullable=True),
    sa.Column('estimated_strategy_capacity', sa.Numeric(), nullable=True),
    sa.Column('lowest_capacity_asset', sa.String(), nullable=True),
    sa.Column('portfolio_turnover', sa.Numeric(), nullable=True),
    sa.Column('equity', sa.Numeric(), nullable=True),
    sa.Column('fees', sa.Numeric(), nullable=True),
    sa.Column('holdings', sa.Numeric(), nullable=True),
    sa.Column('net_profit_runtime', sa.Numeric(), nullable=True),
    sa.Column('probabilistic_sharpe_ratio_runtime', sa.Numeric(), nullable=True),
    sa.Column('return_runtime', sa.Numeric(), nullable=True),
    sa.Column('unrealized', sa.Numeric(), nullable=True),
    sa.Column('volume', sa.Numeric(), nullable=True),
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
    # ### end Alembic commands ###
