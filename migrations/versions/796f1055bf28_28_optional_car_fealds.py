"""Change db model Car - more optional fields now.

Revision ID: 796f1055bf28
Revises: 
Create Date: 2020-11-15 19:02:21.544904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '796f1055bf28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('car', 'body_type',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('car', 'brand',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'city',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'color',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'condition',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'country_now',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'engine',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('car', 'fuel_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'gear_box',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'mileage',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
    op.alter_column('car', 'model',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'picture',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'price',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('car', 'technical_condition',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('car', 'year_of_production',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('car', 'year_of_production',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'technical_condition',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('car', 'price',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'picture',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'model',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'mileage',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    op.alter_column('car', 'gear_box',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'fuel_type',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'engine',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('car', 'country_now',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'condition',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'color',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'city',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'brand',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('car', 'body_type',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
    # ### end Alembic commands ###
