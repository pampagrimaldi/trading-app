"""re-create statistics

Revision ID: 29a6969efb8b
Revises: 10531f98fb46
Create Date: 2023-12-17 17:42:57.270636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '29a6969efb8b'
down_revision: Union[str, None] = '10531f98fb46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backtest_profit_loss', sa.Column('total_trades', sa.Integer(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('average_win', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('average_loss', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('compounding_annual_return', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('drawdown', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('expectancy', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('net_profit', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('sharpe_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('sortino_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('probabilistic_sharpe_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('loss_rate', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('win_rate', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('profit_loss_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('alpha', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('beta', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('annual_standard_deviation', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('annual_variance', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('information_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('tracking_error', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('treynor_ratio', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('total_fees', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('estimated_strategy_capacity', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('lowest_capacity_asset', sa.String(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('portfolio_turnover', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('equity', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('fees', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('holdings', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('net_profit_runtime', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('probabilistic_sharpe_ratio_runtime', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('return_runtime', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('unrealized', sa.Numeric(), nullable=True))
    op.add_column('backtest_profit_loss', sa.Column('volume', sa.Numeric(), nullable=True))
    op.drop_column('backtest_profit_loss', 'profit_loss_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backtest_profit_loss', sa.Column('profit_loss_data', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_column('backtest_profit_loss', 'volume')
    op.drop_column('backtest_profit_loss', 'unrealized')
    op.drop_column('backtest_profit_loss', 'return_runtime')
    op.drop_column('backtest_profit_loss', 'probabilistic_sharpe_ratio_runtime')
    op.drop_column('backtest_profit_loss', 'net_profit_runtime')
    op.drop_column('backtest_profit_loss', 'holdings')
    op.drop_column('backtest_profit_loss', 'fees')
    op.drop_column('backtest_profit_loss', 'equity')
    op.drop_column('backtest_profit_loss', 'portfolio_turnover')
    op.drop_column('backtest_profit_loss', 'lowest_capacity_asset')
    op.drop_column('backtest_profit_loss', 'estimated_strategy_capacity')
    op.drop_column('backtest_profit_loss', 'total_fees')
    op.drop_column('backtest_profit_loss', 'treynor_ratio')
    op.drop_column('backtest_profit_loss', 'tracking_error')
    op.drop_column('backtest_profit_loss', 'information_ratio')
    op.drop_column('backtest_profit_loss', 'annual_variance')
    op.drop_column('backtest_profit_loss', 'annual_standard_deviation')
    op.drop_column('backtest_profit_loss', 'beta')
    op.drop_column('backtest_profit_loss', 'alpha')
    op.drop_column('backtest_profit_loss', 'profit_loss_ratio')
    op.drop_column('backtest_profit_loss', 'win_rate')
    op.drop_column('backtest_profit_loss', 'loss_rate')
    op.drop_column('backtest_profit_loss', 'probabilistic_sharpe_ratio')
    op.drop_column('backtest_profit_loss', 'sortino_ratio')
    op.drop_column('backtest_profit_loss', 'sharpe_ratio')
    op.drop_column('backtest_profit_loss', 'net_profit')
    op.drop_column('backtest_profit_loss', 'expectancy')
    op.drop_column('backtest_profit_loss', 'drawdown')
    op.drop_column('backtest_profit_loss', 'compounding_annual_return')
    op.drop_column('backtest_profit_loss', 'average_loss')
    op.drop_column('backtest_profit_loss', 'average_win')
    op.drop_column('backtest_profit_loss', 'total_trades')
    # ### end Alembic commands ###
