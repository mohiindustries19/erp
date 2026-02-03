"""add expense category master

Revision ID: 9c0e8e2f1a3b
Revises: d31109bc00e1
Create Date: 2026-02-03

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c0e8e2f1a3b'
down_revision = 'd31109bc00e1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'expense_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.UniqueConstraint('name'),
    )
    op.create_index('ix_expense_categories_name', 'expense_categories', ['name'], unique=False)

    bind = op.get_bind()

    # Backfill master list from existing expenses.
    # De-dupe case-insensitively while preserving a nice display form.
    categories_by_key = {'general': 'General'}

    try:
        rows = bind.execute(
            sa.text(
                """
                SELECT DISTINCT expense_category
                FROM expenses
                WHERE expense_category IS NOT NULL
                  AND TRIM(expense_category) <> ''
                """
            )
        ).fetchall()
        for (cat,) in rows:
            if not cat:
                continue
            cleaned = ' '.join(str(cat).strip().split())
            if not cleaned:
                continue
            key = cleaned.lower()

            # Prefer title-ish casing for display if we can.
            if key not in categories_by_key:
                categories_by_key[key] = cleaned
    except Exception:
        # If table doesn't exist yet in some environments, skip backfill.
        pass

    for name in sorted(categories_by_key.values(), key=lambda x: x.lower()):
        bind.execute(
            sa.text(
                """
                INSERT INTO expense_categories (name, is_active)
                VALUES (:name, true)
                """
            ),
            {'name': name},
        )


def downgrade():
    op.drop_index('ix_expense_categories_name', table_name='expense_categories')
    op.drop_table('expense_categories')
