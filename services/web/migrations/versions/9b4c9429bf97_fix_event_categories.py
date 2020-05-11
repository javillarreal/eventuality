"""fix event categories

Revision ID: 9b4c9429bf97
Revises: e58913d0087e
Create Date: 2020-05-11 03:20:03.131806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4c9429bf97'
down_revision = 'e58913d0087e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_subcategories',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['event_category.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('event_id', 'category_id')
    )
    op.drop_table('promoter_users')
    op.drop_table('categories')
    op.add_column('event', sa.Column('main_category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'event_category', ['main_category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'main_category_id')
    op.create_table('categories',
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('main', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['event_category.id'], name='categories_category_id_fkey'),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='categories_event_id_fkey'),
    sa.PrimaryKeyConstraint('event_id', 'category_id', name='categories_pkey')
    )
    op.create_table('promoter_users',
    sa.Column('promoter_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('role', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['promoter_id'], ['promoter.id'], name='promoter_users_promoter_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='promoter_users_user_id_fkey'),
    sa.PrimaryKeyConstraint('promoter_id', 'user_id', name='promoter_users_pkey')
    )
    op.drop_table('event_subcategories')
    # ### end Alembic commands ###
