"""create user table

Revision ID: f4ed422bf152
Revises: 
Create Date: 2023-04-25 10:15:13.057324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f4ed422bf152"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("phone_number", sa.String(20), nullable=False),
        sa.Column("email", sa.String(320)),
        sa.Column("password", sa.String(512), nullable=False),
        sa.Column("active", sa.Boolean(), default=False),
    )


def downgrade() -> None:
    op.drop_table("user")
