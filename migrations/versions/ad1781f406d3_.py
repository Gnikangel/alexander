"""empty message

Revision ID: ad1781f406d3
Revises: 06a01634dff5
Create Date: 2019-07-11 16:14:07.149498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad1781f406d3'
down_revision = '06a01634dff5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('user_id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
