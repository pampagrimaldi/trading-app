"""re-define backest pk

Revision ID: 58d50c1f4e6b
Revises: fd43585c243f
Create Date: 2023-12-20 10:07:07.839107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58d50c1f4e6b'
down_revision: Union[str, None] = 'fd43585c243f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backtest', sa.Column('stock_id', sa.Integer(), nullable=True))
    op.add_column('backtest', sa.Column('strategy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'backtest', 'strategy', ['strategy_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'backtest', 'stock', ['stock_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'backtest', type_='foreignkey')
    op.drop_constraint(None, 'backtest', type_='foreignkey')
    op.drop_column('backtest', 'strategy_id')
    op.drop_column('backtest', 'stock_id')
    # ### end Alembic commands ###
