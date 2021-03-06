"""empty message

Revision ID: 793c0e984fd3
Revises: 0401dd4cf0e9
Create Date: 2020-11-23 00:08:39.606385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '793c0e984fd3'
down_revision = '0401dd4cf0e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('Show', 'show_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('show_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('Show', 'id')
    # ### end Alembic commands ###
