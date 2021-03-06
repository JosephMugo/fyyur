"""empty message

Revision ID: eef2a11c8bde
Revises: c460aaaa2f0e
Create Date: 2020-11-22 12:50:43.037819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eef2a11c8bde'
down_revision = 'c460aaaa2f0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('genre_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Artist', 'Genre', ['genre_id'], ['id'])
    op.add_column('Venue', sa.Column('genre_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'Venue', 'Genre', ['genre_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'genre_id')
    op.drop_constraint(None, 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'genre_id')
    op.drop_table('Genre')
    # ### end Alembic commands ###
