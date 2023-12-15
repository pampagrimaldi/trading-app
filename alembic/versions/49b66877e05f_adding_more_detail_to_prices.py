"""adding more detail to prices

Revision ID: 49b66877e05f
Revises: 667648bba2f5
Create Date: 2023-12-15 13:41:46.962019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49b66877e05f'
down_revision: Union[str, None] = '667648bba2f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter 'close', 'high', and 'low' columns in 'stock_price' table
    op.alter_column('stock_price', 'close', type_=sa.Numeric, existing_type=sa.Numeric(10, 4))
    op.alter_column('stock_price', 'high', type_=sa.Numeric, existing_type=sa.Numeric(10, 4))
    op.alter_column('stock_price', 'low', type_=sa.Numeric, existing_type=sa.Numeric(10, 4))


def downgrade() -> None:
    # Revert 'close', 'high', and 'low' columns in 'stock_price' table back to Numeric(10, 4)
    op.alter_column('stock_price', 'close', type_=sa.Numeric(10, 4), existing_type=sa.Numeric)
    op.alter_column('stock_price', 'high', type_=sa.Numeric(10, 4), existing_type=sa.Numeric)
    op.alter_column('stock_price', 'low', type_=sa.Numeric(10, 4), existing_type=sa.Numeric)