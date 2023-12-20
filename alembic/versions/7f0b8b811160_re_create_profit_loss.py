"""re-create profit-loss

Revision ID: 7f0b8b811160
Revises: 5aa5edc969d6
Create Date: 2023-12-17 22:29:28.964850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7f0b8b811160'
down_revision: Union[str, None] = '5aa5edc969d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backtest_profit_loss', sa.Column('timestamp', sa.DateTime(), nullable=False))
    op.add_column('backtest_profit_loss', sa.Column('value', sa.Numeric(), nullable=False))
    op.drop_column('backtest_profit_loss', 'profit_loss_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backtest_profit_loss', sa.Column('profit_loss_data', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_column('backtest_profit_loss', 'value')
    op.drop_column('backtest_profit_loss', 'timestamp')
    # ### end Alembic commands ###