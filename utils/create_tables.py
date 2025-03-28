import dotenv
from dune_client.client import DuneClient
import os
from dune_client.query import QueryBase

dotenv.load_dotenv()

dune = DuneClient(os.getenv("DUNE_API_KEY_FRACTALVISIONS_SONEIUM"))


# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_newsale",
#     description="Fractalvisions Soneium New Sale Events",
#     schema= [
#         {"name": "listing_creator", "type": "varbinary"},
#         {"name": "listing_id", "type": "uint256"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "buyer", "type": "varbinary"},
#         {"name": "quantity_bought", "type": "uint256"},
#         {"name": "total_price_paid", "type": "uint256"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )

# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_newlisting",
#     description="Fractalvisions Soneium New Listing Events",
#     schema= [
#         {"name": "listing_creator", "type": "varbinary"},
#         {"name": "listing_id", "type": "uint256"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "quantity", "type": "uint256"},
#         {"name": "price_per_token", "type": "uint256"},
#         {"name": "start_timestamp", "type": "varchar"},
#         {"name": "end_timestamp", "type": "varchar"},
#         {"name": "currency", "type": "varbinary"},
#         {"name": "token_type", "type": "varchar"},
#         {"name": "status", "type": "varchar"},
#         {"name": "reserved", "type": "boolean"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )


# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_cancelledlisting",
#     description="Fractalvisions Soneium Cancelled Listing Events",
#     schema= [
#         {"name": "listing_creator", "type": "varbinary"},
#         {"name": "listing_id", "type": "uint256"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )

# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_newoffer",
#     description="Fractalvisions Soneium New Offer Events",
#     schema= [
#         {"name": "offeror", "type": "varbinary"},
#         {"name": "offer_id", "type": "uint256"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "quantity", "type": "uint256"},
#         {"name": "total_price", "type": "uint256"},
#         {"name": "expiration_timestamp", "type": "varchar"},
#         {"name": "currency", "type": "varbinary"},
#         {"name": "token_type", "type": "varchar"},
#         {"name": "status", "type": "varchar"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )


# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_auctionclosed",
#     description="Fractalvisions Soneium Auction Closed Events",
#     schema= [
#         {"name": "auction_id", "type": "uint256"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "closer", "type": "varbinary"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "auction_creator", "type": "varbinary"},
#         {"name": "winning_bidder", "type": "varbinary"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )


# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_newbid",
#     description="Fractalvisions Soneium New Bid Events",
#     schema= [
#         {"name": "auction_id", "type": "uint256"},
#         {"name": "bidder", "type": "varbinary"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "bid_amount", "type": "uint256"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "quantity", "type": "uint256"},
#         {"name": "minimum_bid_amount", "type": "uint256"},
#         {"name": "buyout_bid_amount", "type": "uint256"},
#         {"name": "time_buffer_in_seconds", "type": "uint256"},
#         {"name": "bid_buffer_bps", "type": "uint256"},
#         {"name": "start_timestamp", "type": "varchar"},
#         {"name": "end_timestamp", "type": "varchar"},
#         {"name": "currency", "type": "varbinary"},  
#         {"name": "token_type", "type": "varchar"},
#         {"name": "status", "type": "varchar"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )

# table = dune.create_table(
#     namespace="visionwizards",
#     table_name="soneium_newauction",
#     description="Fractalvisions Soneium New Auction Events",
#     schema= [
#         {"name": "auction_creator", "type": "varbinary"},
#         {"name": "auction_id", "type": "uint256"},
#         {"name": "asset_contract", "type": "varbinary"},
#         {"name": "token_id", "type": "uint256"},
#         {"name": "quantity", "type": "uint256"},
#         {"name": "minimum_bid_amount", "type": "uint256"},
#         {"name": "buyout_bid_amount", "type": "uint256"},
#         {"name": "time_buffer_in_seconds", "type": "uint256"},
#         {"name": "bid_buffer_bps", "type": "uint256"},
#         {"name": "start_timestamp", "type": "varchar"},
#         {"name": "end_timestamp", "type": "varchar"},
#         {"name": "currency", "type": "varbinary"},  
#         {"name": "token_type", "type": "varchar"},
#         {"name": "status", "type": "varchar"},
#         {"name": "gas_price", "type": "uint256"},
#         {"name": "gas_used", "type": "uint256"},
#         {"name": "block_number", "type": "uint256"},
#         {"name": "timestamp", "type": "varchar"},
#         {"name": "transaction_hash", "type": "varbinary"},
#         {"name": "event_type", "type": "varchar"}
#     ],
#     is_private=False
# )
