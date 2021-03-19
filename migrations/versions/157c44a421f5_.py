"""empty message

Revision ID: 157c44a421f5
Revises: 990076f6ad5e
Create Date: 2021-03-18 22:43:16.702827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157c44a421f5'
down_revision = '990076f6ad5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'cost',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('items', 'picture_url',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=600),
               existing_nullable=True)
    op.alter_column('users', 'address',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=400),
               existing_nullable=True)
    op.alter_column('users', 'profile_pic_url',
               existing_type=sa.VARCHAR(length=400),
               type_=sa.String(length=600),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'profile_pic_url',
               existing_type=sa.String(length=600),
               type_=sa.VARCHAR(length=400),
               existing_nullable=True)
    op.alter_column('users', 'address',
               existing_type=sa.String(length=400),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    op.alter_column('items', 'picture_url',
               existing_type=sa.String(length=600),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    op.alter_column('items', 'cost',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
