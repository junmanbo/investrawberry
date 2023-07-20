from app.db.session import SessionLocal

from app.crud.asset_type import asset_type
from app.schemas.asset_type import AssetTypeCreate


# Create a new session
session = SessionLocal()

asset_data_list = [
    {"asset_nm": "STOCK", "asset_knm": "주식"},
    {"asset_nm": "CRYPTO", "asset_knm": "코인"},
    {"asset_nm": "BOND", "asset_knm": "채권"},
]

for data in asset_data_list:
    print(data)
    asset_type_data = AssetTypeCreate(
        asset_nm=data['asset_nm'],
        asset_knm=data['asset_knm'],
    )
    # Add the new Ticker object to the database using the CRUD object
    asset_type.create(session, obj_in=asset_type_data)

# Close the session
session.close()


