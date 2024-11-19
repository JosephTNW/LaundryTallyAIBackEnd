"""empty message

Revision ID: e31c843bddf7
Revises: 52bf0fb17cd1
Create Date: 2024-07-11 15:02:04.814560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e31c843bddf7'
down_revision = '52bf0fb17cd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('laundry', schema=None) as batch_op:
        batch_op.alter_column('laundry_days',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('laundry', schema=None) as batch_op:
        batch_op.alter_column('laundry_days',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###