"""empty message

Revision ID: ed8b788fd93d
Revises: eef2a11c8bde
Create Date: 2020-11-22 14:04:04.566132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8b788fd93d'
down_revision = 'eef2a11c8bde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_genre',
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('venue_id', 'genre_id')
    )
    op.drop_constraint('Artist_genre_id_fkey', 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'genre_id')
    op.alter_column('Genre', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('Venue_genre_id_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'genre_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Venue_genre_id_fkey', 'Venue', 'Genre', ['genre_id'], ['id'])
    op.alter_column('Genre', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('Artist', sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Artist_genre_id_fkey', 'Artist', 'Genre', ['genre_id'], ['id'])
    op.drop_table('venue_genre')
    # ### end Alembic commands ###
