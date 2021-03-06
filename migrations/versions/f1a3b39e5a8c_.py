"""empty message

Revision ID: f1a3b39e5a8c
Revises: 9bc3e3445e50
Create Date: 2020-11-23 11:34:44.839178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a3b39e5a8c'
down_revision = '9bc3e3445e50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'show_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('show_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
