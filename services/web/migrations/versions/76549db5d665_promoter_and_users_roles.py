"""promoter and users roles

Revision ID: 76549db5d665
Revises: 0b826a01e30d
Create Date: 2020-05-09 20:50:51.660906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76549db5d665'
down_revision = '0b826a01e30d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event_category', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    op.drop_index('ix_event_category_name', table_name='event_category')
    op.create_index(op.f('ix_event_category_name'), 'event_category', ['name'], unique=True)
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.drop_constraint('user_username_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_column('user', 'is_admin')
    op.drop_column('user', 'is_active')
    op.drop_index(op.f('ix_event_category_name'), table_name='event_category')
    op.create_index('ix_event_category_name', 'event_category', ['name'], unique=False)
    op.alter_column('event_category', 'name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    # ### end Alembic commands ###