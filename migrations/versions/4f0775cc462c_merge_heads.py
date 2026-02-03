"""merge heads

Revision ID: 4f0775cc462c
Revises: 4d600ea50fdd, 9c0e8e2f1a3b, add_barcode_001
Create Date: 2026-02-03 00:48:21.074194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f0775cc462c'
down_revision = ('4d600ea50fdd', '9c0e8e2f1a3b', 'add_barcode_001')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
