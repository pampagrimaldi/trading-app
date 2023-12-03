"""delete volum duplice s_price

Revision ID: e5874327b746
Revises: 6212ee492ee6
Create Date: 2023-12-03 11:12:17.424555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5874327b746'
down_revision: Union[str, None] = '6212ee492ee6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stock_price', 'volume',
               existing_type=sa.BIGINT(),
               type_=sa.Numeric(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('stock_price', 'volume',
               existing_type=sa.Numeric(),
               type_=sa.BIGINT(),
               existing_nullable=False)
    # ### end Alembic commands ###