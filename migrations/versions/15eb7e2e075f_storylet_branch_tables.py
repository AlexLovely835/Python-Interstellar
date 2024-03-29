"""storylet branch tables

Revision ID: 15eb7e2e075f
Revises: b27fd29fdedf
Create Date: 2022-11-16 20:15:33.229796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15eb7e2e075f'
down_revision = 'b27fd29fdedf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storylet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('escapable', sa.Boolean(), nullable=True),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('branch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('button_text', sa.String(), nullable=True),
    sa.Column('storylet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['storylet_id'], ['storylet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('branch')
    op.drop_table('storylet')
    # ### end Alembic commands ###
