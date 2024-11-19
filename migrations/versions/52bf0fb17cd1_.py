"""empty message

Revision ID: 52bf0fb17cd1
Revises: 26f8bc9eccef
Create Date: 2024-07-06 21:51:33.752626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52bf0fb17cd1'
down_revision = '26f8bc9eccef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('launderer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('l_pic', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('launderer', schema=None) as batch_op:
        batch_op.drop_column('l_pic')

    # ### end Alembic commands ###