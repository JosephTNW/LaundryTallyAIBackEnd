"""modify launderer

Revision ID: e2516f887e0e
Revises: 8a0909f20d42
Create Date: 2024-06-21 07:30:33.630700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2516f887e0e'
down_revision = '8a0909f20d42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('launderer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('has_delivery', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('inputted_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('launderer', schema=None) as batch_op:
        batch_op.drop_column('inputted_at')
        batch_op.drop_column('has_delivery')

    # ### end Alembic commands ###
