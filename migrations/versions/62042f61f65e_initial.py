"""initial

Revision ID: 62042f61f65e
Revises: 
Create Date: 2024-09-20 09:53:12.757477

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '62042f61f65e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
