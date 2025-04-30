"""Add active flag to Treatment

Revision ID: 532eab31bc95
Revises: e441dadd5e04
Create Date: 2025-04-27 16:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '532eab31bc95'
down_revision = 'e441dadd5e04'
branch_labels = None
depends_on = None


def upgrade():
    # 1) active カラムを NOT NULL, server_default=TRUE で追加
    with op.batch_alter_table('treatments') as batch_op:
        batch_op.add_column(
            sa.Column(
                'active',
                sa.Boolean(),
                nullable=False,
                server_default=sa.text('1')     # SQLite では TRUE は 1
            )
        )
    # 2) デフォルト値を解除（以後の INSERT はモデルの default が使われる）
    with op.batch_alter_table('treatments') as batch_op:
        batch_op.alter_column(
            'active',
            server_default=None
        )


def downgrade():
    # active カラムを削除してロールバック
    with op.batch_alter_table('treatments') as batch_op:
        batch_op.drop_column('active')
