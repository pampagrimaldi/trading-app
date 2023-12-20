"""re-create statistics

Revision ID: 10531f98fb46
Revises: 9548dce86c28
Create Date: 2023-12-17 17:40:57.499155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10531f98fb46'
down_revision: Union[str, None] = '9548dce86c28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_backtest_statistics_id', table_name='backtest_statistics')
    op.drop_table('backtest_statistics')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('backtest_statistics',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('backtest_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('statistic_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('statistic_value', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['backtest_id'], ['backtest.id'], name='backtest_statistics_backtest_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='backtest_statistics_pkey')
    )
    op.create_index('ix_backtest_statistics_id', 'backtest_statistics', ['id'], unique=False)
    # ### end Alembic commands ###