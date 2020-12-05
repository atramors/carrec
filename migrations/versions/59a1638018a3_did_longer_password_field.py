"""Did longer password field

Revision ID: 59a1638018a3
Revises: 796f1055bf28
Create Date: 2020-12-04 22:08:16.539978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59a1638018a3"
down_revision = "796f1055bf28"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'password',
        existing_type=sa.VARCHAR(length=80),
        nullable=False)


def downgrade():
    op.alter_column('user', 'password',
        existing_type=sa.VARCHAR(length=60),
        nullable=False)
