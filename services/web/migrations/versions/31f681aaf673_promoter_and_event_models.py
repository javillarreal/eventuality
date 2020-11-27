"""promoter and event models

Revision ID: 31f681aaf673
Revises: 76549db5d665
Create Date: 2020-05-09 22:22:38.871624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31f681aaf673'
down_revision = '76549db5d665'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('longitude', sa.Float(precision=9), nullable=True),
    sa.Column('latitude', sa.Float(precision=9), nullable=True),
    sa.Column('datetime_from', sa.DateTime(), nullable=False),
    sa.Column('datetime_to', sa.DateTime(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('main', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['event_category.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('event_id', 'category_id')
    )
    op.create_table('promoter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('longitude', sa.Float(precision=9), nullable=True),
    sa.Column('latitude', sa.Float(precision=9), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('main_category', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['main_category'], ['event_category.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_promoter_name'), 'promoter', ['name'], unique=False)
    op.create_table('promoters',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('promoter_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['promoter_id'], ['promoter.id'], ),
    sa.PrimaryKeyConstraint('event_id', 'promoter_id')
    )
    op.create_table('users',
    sa.Column('promoter_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['promoter_id'], ['promoter.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('promoter_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('promoters')
    op.drop_index(op.f('ix_promoter_name'), table_name='promoter')
    op.drop_table('promoter')
    op.drop_table('categories')
    op.drop_table('event')
    # ### end Alembic commands ###
