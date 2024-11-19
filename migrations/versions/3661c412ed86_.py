"""empty message

Revision ID: 3661c412ed86
Revises: 7b27c0670af9
Create Date: 2024-06-29 18:38:46.750750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3661c412ed86'
down_revision = '7b27c0670af9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('launderer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('phone_num', sa.String(length=50), nullable=True),
    sa.Column('has_whatsapp', sa.Boolean(), nullable=True),
    sa.Column('has_delivery', sa.Boolean(), nullable=True),
    sa.Column('inputted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('clothes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('color', sa.String(length=50), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('cloth_pic', sa.String(length=200), nullable=True),
    sa.Column('inputted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('laundry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('launderer', sa.Integer(), nullable=True),
    sa.Column('bill_pic', sa.String(length=200), nullable=True),
    sa.Column('laundered_at', sa.DateTime(), nullable=True),
    sa.Column('laundry_days', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['launderer'], ['launderer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('laundried_clothes',
    sa.Column('laundry_id', sa.Integer(), nullable=True),
    sa.Column('clothes_id', sa.Integer(), nullable=True),
    sa.Column('returned', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['clothes_id'], ['clothes.id'], ),
    sa.ForeignKeyConstraint(['laundry_id'], ['laundry.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('laundried_clothes')
    op.drop_table('laundry')
    op.drop_table('clothes')
    op.drop_table('user')
    op.drop_table('launderer')
    # ### end Alembic commands ###
