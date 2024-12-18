"""clothes returned

Revision ID: 7b27c0670af9
Revises: e2516f887e0e
Create Date: 2024-06-23 14:19:53.395389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b27c0670af9'
down_revision = 'e2516f887e0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('laundried_clothes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('returned', sa.Boolean(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    with op.batch_alter_table('laundried_clothes', schema=None) as batch_op:
        batch_op.drop_column('returned')

    # ### end Alembic commands ###
