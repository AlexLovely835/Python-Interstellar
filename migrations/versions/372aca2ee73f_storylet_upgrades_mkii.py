"""storylet upgrades mkii

Revision ID: 372aca2ee73f
Revises: bd7cac6d8d4d
Create Date: 2022-11-18 12:38:56.782676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '372aca2ee73f'
down_revision = 'bd7cac6d8d4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storylet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('area', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('urgency', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('notes', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('storylet', schema=None) as batch_op:
        batch_op.drop_column('notes')
        batch_op.drop_column('order')
        batch_op.drop_column('urgency')
        batch_op.drop_column('area')

    # ### end Alembic commands ###
