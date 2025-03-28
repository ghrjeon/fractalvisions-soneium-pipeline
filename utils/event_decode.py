import pandas as pd
from web3 import Web3
from eth_abi import decode


def decode_AuctionClosed(data):
    '''
    Decode AuctionClosed
    topic0: 0x7003143824ad94e684efcfd33e097dd7cd0e67243daf20f345f5186a9a7ba00a

    AuctionClosed(
        uint256 indexed auctionId,
        address indexed assetContract,
        address indexed closer,
        uint256 tokenId,
        address auctionCreator,
        address winningBidder,
    )
    '''

    df = pd.DataFrame(data)

    # Extract topics
    df['auction_id'] = df['topics'].apply(lambda x: int(x[1], 16))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[2][-40:]))
    df['closer'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))

    # Define the non_indexed_types variables for the Auction struct
    non_indexed_types = ['uint256', 'address', 'address']
    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))

    # Decode the struct fields
    # Create separate columns for each decoded value
    df['token_id'] = df['decoded_data'].apply(lambda x: x[0])
    df['auction_creator'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[1]))
    df['winning_bidder'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[2]))

    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))
    df['transaction_hash'] = df['transactionHash']

    df = df[['auction_id', 'asset_contract', 'closer', 'token_id', 'auction_creator', 'winning_bidder', 'gas_price', 'gas_used', 'block_number', 'timestamp', 'transaction_hash']]

    return df

def decode_NewBid(data):
    '''
    Decode NewBid
    topic0: 0x433a278e1c55403e97ab8ffef6ce9fddd5d1fb2695745bbc3affbe0b8106ec6b


    NewBid(
        uint256 indexed auctionId,
        address indexed bidder,
        address indexed assetContract,
        uint256 bidAmount
        (uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,address,address,address,uint256,uint256) auction
    )
    Auction is a struct with the following fields:
    - uint256 auctionId
    - uint256 tokenId
    - uint256 quantity
    - uint256 minimumBidAmount
    - uint256 buyoutBidAmount
    - uint256 timeBufferInSeconds
    - uint256 bidBufferBps
    - uint256 startTimestamp
    - uint256 endTimestamp
    - address auctionCreator
    - address assetContract
    - address currency
    - uint256 tokenType
    - uint256 status
    '''

    df = pd.DataFrame(data)

    # Extract topics
    df['auction_id'] = df['topics'].apply(lambda x: int(x[1], 16))
    df['bidder'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[2][-40:]))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))

    # Define the non_indexed_types variables for the Auction struct
    non_indexed_types = ['uint256','uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'address', 'address', 'address', 'uint256', 'uint256']
    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))

    # Decode the struct fields
    # Create separate columns for each decoded value
    df['bid_amount'] = df['decoded_data'].apply(lambda x: x[0])
    df['auction_id_decoded'] = df['decoded_data'].apply(lambda x: x[1])
    df['token_id'] = df['decoded_data'].apply(lambda x: x[2])
    df['quantity'] = df['decoded_data'].apply(lambda x: x[3])
    df['minimum_bid_amount'] = df['decoded_data'].apply(lambda x: x[4])
    df['buyout_bid_amount'] = df['decoded_data'].apply(lambda x: x[5])
    df['time_buffer_in_seconds'] = df['decoded_data'].apply(lambda x: x[6])
    df['bid_buffer_bps'] = df['decoded_data'].apply(lambda x: x[7])
    df['start_timestamp'] = df['decoded_data'].apply(lambda x: x[8])
    df['end_timestamp'] = df['decoded_data'].apply(lambda x: x[9])
    df['auction_creator_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[10]))
    df['asset_contract_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[11]))
    df['currency'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[12]))
    df['token_type'] = df['decoded_data'].apply(lambda x: x[13])
    df['status'] = df['decoded_data'].apply(lambda x: x[14])

   # Map enum values to their readable names 
    token_type_names = {
        0: "ERC1155",
        1: "ERC721"
    }
    
    status_names = {
        0: "CREATED",
        1: "ACTIVE", 
        2: "CANCELLED",
        3: "EXECUTED"
    }

    df['token_type'] = df['token_type'].map(token_type_names)
    df['status'] = df['status'].map(status_names)

    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))
    df['transaction_hash'] = df['transactionHash']

    # Collate data needed
    df = df[['auction_id', 'bidder', 'asset_contract', 'bid_amount', 'token_id', 'quantity', 'minimum_bid_amount', 'buyout_bid_amount', 'time_buffer_in_seconds', 'bid_buffer_bps', 'start_timestamp', 'end_timestamp', 'currency', 'token_type', 'status',
             'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]

    return df


def decode_NewAuction(data):
    '''
    Decode NewAuction
    topic0: 0x5afd538bb1e7fc354db91c5dc4876ea2321a22fb8fbb69c84bda1f84ce1f45df

    NewAuction(
        address indexed auctionCreator,
        uint256 indexed auctionId,
        address indexed assetContract,
        (uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,address,address,address,uint256,uint256) auction
    )
    Auction is a struct with the following fields:
        uint256 auctionId,
        uint256 tokenId,
        uint256 quantity,
        uint256 minimumBidAmount,
        uint256 buyoutBidAmount,
        uint256 timeBufferInSeconds,
        uint256 bidBufferBps,
        uint256 startTimestamp,
        uint256 endTimestamp,
        address auctionCreator,
        address assetContract,
        address currency,
        uint256 tokenType,
        uint256 status
    '''
    df = pd.DataFrame(data)

    # Extract topics
    df['auction_creator'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[1][-40:]))
    df['auction_id'] = df['topics'].apply(lambda x: int(x[2], 16))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))
    
    # Define the non_indexed_types variables for the Auction struct
    non_indexed_types = ['uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'address', 'address', 'address', 'uint256', 'uint256']

    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))
    
    # Decode the struct fields
    # Create separate columns for each decoded value
    df['auction_id_decoded'] = df['decoded_data'].apply(lambda x: x[0])
    df['token_id'] = df['decoded_data'].apply(lambda x: x[1])
    df['quantity'] = df['decoded_data'].apply(lambda x: x[2])
    df['minimum_bid_amount'] = df['decoded_data'].apply(lambda x: x[3])
    df['buyout_bid_amount'] = df['decoded_data'].apply(lambda x: x[4])
    df['time_buffer_in_seconds'] = df['decoded_data'].apply(lambda x: x[5])
    df['bid_buffer_bps'] = df['decoded_data'].apply(lambda x: x[6])
    df['start_timestamp'] = df['decoded_data'].apply(lambda x: x[7])
    df['end_timestamp'] = df['decoded_data'].apply(lambda x: x[8])
    df['auction_creator_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[9]))
    df['asset_contract_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[10]))
    df['currency'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[11]))
    df['token_type'] = df['decoded_data'].apply(lambda x: x[12])
    df['status'] = df['decoded_data'].apply(lambda x: x[13])

    # Map enum values to their readable names
    token_type_names = {
        0: "ERC1155",
        1: "ERC721"
    }
    
    status_names = {
        0: "CREATED",
        1: "ACTIVE", 
        2: "CANCELLED",
        3: "EXECUTED"
    }

    df['token_type'] = df['token_type'].map(token_type_names)
    df['status'] = df['status'].map(status_names)

    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))
    df['transaction_hash'] = df['transactionHash']

    # Collate data needed
    df = df[['auction_creator', 'auction_id', 'asset_contract', 'token_id', 'quantity', 'minimum_bid_amount', 'buyout_bid_amount', 'time_buffer_in_seconds', 'bid_buffer_bps', 'start_timestamp', 'end_timestamp', 'currency', 'token_type', 'status',
             'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]

    return df


def decode_NewListing(data):

    '''
    Decode NewListing
    topic0: 0x783dd929408cfd2d118397c912a4b576683c43b41b015e3d7c212bac0cd0e7c7

    NewListing(
        address indexed listingCreator,
        uint256 indexed listingId,
        address indexed assetContract,
        (uint256,uint256,uint256,uint256,uint128,uint128,address,address,address,uint8,uint8,bool) listing
    )
    Listing is a struct with the following fields:
    - uint256 listingId
    - uint256 tokenId
    - uint256 quantity
    - uint256 pricePerToken
    - uint128 startTimestamp
    - uint128 endTimestamp
    - address listingCreator
    - address assetContract
    - address currency
    - enum IDirectListings.TokenType tokenType (uint8)
    - enum IDirectListings.Status status (uint8)
    - bool reserved
    '''

    df = pd.DataFrame(data)

    # Extract topics
    df['listing_creator'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[1][-40:]))
    df['listing_id'] = df['topics'].apply(lambda x: int(x[2], 16))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))

    # Define the non_indexed_types variables for the Listing struct
    non_indexed_types = ['uint256', 'uint256', 'uint256', 'uint256', 'uint128', 'uint128', 'address', 'address', 'address', 'uint8', 'uint8', 'bool']  

    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))

    # Decode the struct fields
    # Create separate columns for each decoded value
    df['listing_id_decoded'] = df['decoded_data'].apply(lambda x: x[0])
    df['token_id'] = df['decoded_data'].apply(lambda x: x[1])
    df['quantity'] = df['decoded_data'].apply(lambda x: x[2])
    df['price_per_token'] = df['decoded_data'].apply(lambda x: x[3])
    df['start_timestamp'] = df['decoded_data'].apply(lambda x: x[4])
    df['end_timestamp'] = df['decoded_data'].apply(lambda x: x[5])
    df['listing_creator_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[6]))
    df['asset_contract_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[7]))
    df['currency'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[8]))
    df['token_type'] = df['decoded_data'].apply(lambda x: x[9])
    df['status'] = df['decoded_data'].apply(lambda x: x[10])
    df['reserved'] = df['decoded_data'].apply(lambda x: x[11])

    # Map enum values to their readable names 
    token_type_names = {
        0: "ERC1155",
        1: "ERC721"
    }
    
    status_names = {
        0: "CREATED",
        1: "ACTIVE", 
        2: "CANCELLED",
        3: "EXECUTED"
    }

    df['token_type'] = df['token_type'].map(token_type_names)
    df['status'] = df['status'].map(status_names)
    

    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))
    df['transaction_hash'] = df['transactionHash']

    # Collate data needed
    df = df[['listing_creator', 'listing_id', 'asset_contract', 'token_id', 'quantity', 'price_per_token', 
             'start_timestamp', 'end_timestamp', 'currency', 'token_type', 'status', 'reserved',
             'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]

    return df

def decode_NewSale(data):
    '''
    Decode NewSale
    topic0: 0xf6e03f1c408cfd2d118397c912a4b576683c43b41b015e3d7c212bac0cd0e7c7
    NewSale(address,uint256,address,uint256,address,uint256,uint256)
    NewSale(
        address indexed buyer,
        uint256 indexed listingId,
        address indexed assetContract,
        uint256 tokenId,
        uint256 quantityBought,
        uint256 totalPricePaid
    )    
    '''
    df = pd.DataFrame(data)

    # Extract topics
    df['listing_creator'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[1][-40:]))
    df['listing_id'] = df['topics'].apply(lambda x: int(x[2], 16))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))

    # Define the non_indexed_types variables for NewSale
    non_indexed_types = ['uint256', 'address', 'uint256', 'uint256']  

    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))

    # Create separate columns for each decoded value
    df['token_id'] = df['decoded_data'].apply(lambda x: x[0])
    df['buyer'] = df['decoded_data'].apply(lambda x: x[1])
    df['quantity_bought'] = df['decoded_data'].apply(lambda x: x[2])
    df['total_price_paid'] = df['decoded_data'].apply(lambda x: x[3])
    
    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))

    # Convert timestamp from hex to int if it starts with '0x'
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))

    df['transaction_hash'] = df['transactionHash']

    # colalte data needed

    df = df[['listing_creator', 'listing_id', 'asset_contract', 'token_id', 'buyer', 'quantity_bought', 'total_price_paid',
             'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]
   
    return df


def decode_CancelledListing(data):
    '''
    Decode NewCancelledListingSale
    topic0: 0xf6e9b23c95dec70093b0abc1cf13bc5d35c9af03743f941904a4ef664e0119fb  
    CancelledListing(address indexed listingCreator, uint256 indexed listingId)
    CancelledListing(
        address indexed listingCreator,
        uint256 indexed listingId
    )    
    '''
    df = pd.DataFrame(data)

    # Extract topics
    df['listing_creator'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[1][-40:]))
    df['listing_id'] = df['topics'].apply(lambda x: int(x[2], 16))

    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))

    # Convert timestamp from hex to int if it starts with '0x'
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))
    df['transaction_hash'] = df['transactionHash']
    # colalte data needed

    df = df[['listing_creator', 'listing_id',
             'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]

    return df



def decode_NewOffer(data):
    '''
    Decode NewOffer
    topic0: 0x8a597d224658d6f05ad676ddd666a25096b0bf7eff59d873ccbe943f8a3313ae
    NewOffer (index_topic_1 address offeror, index_topic_2 uint256 offerId, index_topic_3 address assetContract, tuple offer)
    NewOffer(
        address indexed offeror,
        uint256 indexed offerId,
        address indexed assetContract,
        tuple offer
    ) 
    Offer is a struct with the following fields:
    - uint256 offerId
    - uint256 tokenId
    - uint256 quantity
    - uint256 totalPrice
    - uint128 expirationTimestamp
    - address offeror
    - address assetContract
    - address currency
    - enum IDirectListings.TokenType tokenType (uint8)
    - enum IDirectListings.Status status (uint8)
    '''

    df = pd.DataFrame(data)

    # Extract topics
    df['offeror'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[1][-40:]))
    df['offer_id'] = df['topics'].apply(lambda x: int(x[2], 16))
    df['asset_contract'] = df['topics'].apply(lambda x: Web3.to_checksum_address('0x' + x[3][-40:]))

    # Define the non_indexed_types variables for NewSale
    non_indexed_types = ['uint256', 'uint256', 'uint256', 'uint256', 'uint128', 'address', 'address', 'address', 'uint8', 'uint8']  

    # Decode the data column
    df['decoded_data'] = df['data'].apply(lambda x: decode(non_indexed_types, bytes.fromhex(x[2:] if x.startswith('0x') else x)))

    # Create separate columns for each decoded value
    df['offer_id'] = df['decoded_data'].apply(lambda x: x[0])
    df['token_id'] = df['decoded_data'].apply(lambda x: x[1])
    df['quantity'] = df['decoded_data'].apply(lambda x: x[2])
    df['total_price'] = df['decoded_data'].apply(lambda x: x[3])
    df['expiration_timestamp'] = df['decoded_data'].apply(lambda x: x[4])
    df['offeror_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[5]))
    df['asset_contract_decoded'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[6]))
    df['currency'] = df['decoded_data'].apply(lambda x: Web3.to_checksum_address(x[7]))
    df['token_type'] = df['decoded_data'].apply(lambda x: x[8])
    df['status'] = df['decoded_data'].apply(lambda x: x[9])
    
    # Map enum values to their readable names
    token_type_names = {
        0: "ERC1155",
        1: "ERC721"
    }
    
    status_names = {
        0: "CREATED",
        1: "ACTIVE", 
        2: "CANCELLED",
        3: "EXECUTED"
    }

    df['token_type'] = df['token_type'].map(token_type_names)
    df['status'] = df['status'].map(status_names)


    df['gas_price'] = df['gasPrice'].apply(lambda x: int(x, 16))
    df['gas_used'] = df['gasUsed'].apply(lambda x: int(x, 16))

    # Convert timestamp from hex to int if it starts with '0x'
    df['timestamp'] = df['timeStamp'].apply(lambda x: int(x, 16))
    df['block_number'] = df['blockNumber'].apply(lambda x: int(x, 16))

    df['transaction_hash'] = df['transactionHash']

    # colalte data needed

    df = df[['offeror', 'offer_id', 'asset_contract', 'token_id', 'quantity', 'total_price', 'expiration_timestamp',
             'currency', 'token_type', 'status', 'gas_price', 'gas_used', 'block_number', 'timestamp','transaction_hash']]

    return df