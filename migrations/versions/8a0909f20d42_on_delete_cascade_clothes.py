"""on delete cascade clothes

Revision ID: 8a0909f20d42
Revises: d9f79459b54d
Create Date: 2024-06-21 00:40:50.683909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a0909f20d42'
down_revision = 'd9f79459b54d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clothes', schema=None) as batch_op:
        batch_op.drop_constraint('clothes_owner_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['owner'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clothes', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('clothes_owner_fkey', 'user', ['owner'], ['id'])

    # ### end Alembic commands ###
