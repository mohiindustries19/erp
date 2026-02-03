"""Add barcode fields to products

Revision ID: add_barcode_001
Revises: 
Create Date: 2024-02-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'add_barcode_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_columns = {c['name'] for c in inspector.get_columns('products')}

    # Add barcode columns to products table (safe if rerun)
    with op.batch_alter_table('products') as batch_op:
        if 'ean_barcode' not in existing_columns:
            batch_op.add_column(sa.Column('ean_barcode', sa.String(length=13), nullable=True))
        if 'barcode_source' not in existing_columns:
            batch_op.add_column(sa.Column('barcode_source', sa.String(length=32), nullable=True))
        if 'barcode_registered_date' not in existing_columns:
            batch_op.add_column(sa.Column('barcode_registered_date', sa.Date(), nullable=True))

    existing_indexes = {ix['name'] for ix in inspector.get_indexes('products')}
    if 'ix_products_ean_barcode' not in existing_indexes:
        op.create_index('ix_products_ean_barcode', 'products', ['ean_barcode'], unique=True)


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_columns = {c['name'] for c in inspector.get_columns('products')}
    existing_indexes = {ix['name'] for ix in inspector.get_indexes('products')}

    # Remove index if present
    if 'ix_products_ean_barcode' in existing_indexes:
        op.drop_index('ix_products_ean_barcode', table_name='products')

    # Remove columns if present
    with op.batch_alter_table('products') as batch_op:
        if 'barcode_registered_date' in existing_columns:
            batch_op.drop_column('barcode_registered_date')
        if 'barcode_source' in existing_columns:
            batch_op.drop_column('barcode_source')
        if 'ean_barcode' in existing_columns:
            batch_op.drop_column('ean_barcode')
