"""empty message

Revision ID: a218a1d4a8d1
Revises: 
Create Date: 2023-08-11 09:44:23.606842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a218a1d4a8d1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("ticker_asset_type_id_fkey", "ticker", type_="foreignkey")
    op.drop_column("ticker", "asset_type_id")
    op.drop_index("ix_asset_type_id", table_name="asset_type")
    op.drop_table("asset_type")
    op.execute("CREATE TYPE asset_type AS ENUM ('kr_stock', 'us_stock', 'crypto')")
    op.add_column(
        "ticker",
        sa.Column(
            "asset_type",
            sa.Enum("kr_stock", "us_stock", "crypto", name="asset_type"),
            nullable=True,
        ),
    )
    op.execute("CREATE TYPE order_type AS ENUM ('market', 'limit')")
    op.execute(
        "ALTER TABLE transaction ALTER COLUMN order_type TYPE order_type USING order_type::order_type"
    )
    op.alter_column(
        "transaction",
        "order_type",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum("market", "limit", name="order_type"),
        existing_nullable=True,
    )
    op.execute("CREATE TYPE side AS ENUM ('buy', 'sell')")
    op.execute("ALTER TABLE transaction ALTER COLUMN side TYPE side USING side::side")
    op.alter_column(
        "transaction",
        "side",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum("buy", "sell", name="side"),
        existing_nullable=False,
    )
    op.execute("CREATE TYPE status AS ENUM ('open', 'canceled', 'closed')")
    op.execute(
        "ALTER TABLE transaction ALTER COLUMN status TYPE status USING status::status"
    )
    op.alter_column(
        "transaction",
        "status",
        existing_type=sa.VARCHAR(length=10),
        type_=sa.Enum("open", "canceled", "closed", name="status"),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "transaction",
        "status",
        existing_type=sa.Enum("open", "canceled", "closed", name="status"),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    op.alter_column(
        "transaction",
        "side",
        existing_type=sa.Enum("buy", "sell", name="side"),
        type_=sa.VARCHAR(length=10),
        existing_nullable=False,
    )
    op.alter_column(
        "transaction",
        "order_type",
        existing_type=sa.Enum("market", "limit", name="order_type"),
        type_=sa.VARCHAR(length=10),
        existing_nullable=True,
    )
    op.add_column(
        "ticker",
        sa.Column("asset_type_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "ticker_asset_type_id_fkey", "ticker", "asset_type", ["asset_type_id"], ["id"]
    )
    op.drop_column("ticker", "asset_type")
    op.create_table(
        "asset_type",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "asset_nm", sa.VARCHAR(length=20), autoincrement=False, nullable=False
        ),
        sa.Column(
            "asset_knm", sa.VARCHAR(length=20), autoincrement=False, nullable=False
        ),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="asset_type_pkey"),
        sa.UniqueConstraint("asset_knm", name="asset_type_asset_knm_key"),
        sa.UniqueConstraint("asset_nm", name="asset_type_asset_nm_key"),
    )
    op.create_index("ix_asset_type_id", "asset_type", ["id"], unique=False)
    # ### end Alembic commands ###
