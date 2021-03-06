"""empty message

Revision ID: 9a5ada577106
Revises: 030b84f4aa43
Create Date: 2020-07-23 05:01:00.877086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a5ada577106'
down_revision = '030b84f4aa43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email_verified', sa.Boolean(), nullable=True))
    op.drop_column('user', 'emai_verified')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('emai_verified', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('user', 'email_verified')
    # ### end Alembic commands ###
