"""empty message

Revision ID: ce319e906433
Revises: 740524d8db37
Create Date: 2021-07-28 14:20:59.625208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce319e906433'
down_revision = '740524d8db37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('last_name', sa.String(length=140), nullable=True),
    sa.Column('phone', sa.String(length=140), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('book')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=140), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=140), nullable=True),
    sa.Column('phone', sa.VARCHAR(length=140), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('note')
    # ### end Alembic commands ###
