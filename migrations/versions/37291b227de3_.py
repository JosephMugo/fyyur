"""empty message

Revision ID: 37291b227de3
Revises: 03e917e06016
Create Date: 2020-11-21 23:02:58.742259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37291b227de3'
down_revision = '03e917e06016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    # ### end Alembic commands ###
