"""add followers

Revision ID: 934177726c72
Revises: c5eeada1ae1c
Create Date: 2018-03-11 13:06:44.361160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '934177726c72'
down_revision = 'c5eeada1ae1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
