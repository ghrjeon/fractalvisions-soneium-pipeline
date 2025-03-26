topic_mapping = [
    {
        "topic0": "0xf6e03f1c408cfd2d118397c912a4b576683c43b41b015e3d7c212bac0cd0e7c7",
        "event_type": "NewSale",
        "table_name": "soneium_newsale",
        "decoder": "decode_NewSale"
    },
    {
        "topic0": "0xef309e3999c4dd6a4c1e4af6221896b7e5ccf9e7fc4fe5b218b883ce9190d7ad",
        "event_type": "NewListing", 
        "table_name": "soneium_newlisting",
        "decoder": "decode_NewListing"
    },
    {
        "topic0": "0xf6e9b23c95dec70093b0abc1cf13bc5d35c9af03743f941904a4ef664e0119fb",
        "event_type": "CancelledListing",
        "table_name": "soneium_cancelledlisting",
        "decoder": "decode_CancelledListing"
    },
    {
        "topic0": "0x8a597d224658d6f05ad676ddd666a25096b0bf7eff59d873ccbe943f8a3313ae",
        "event_type": "NewOffer",
        "table_name": "soneium_newoffer",
        "decoder": "decode_NewOffer"
    }
]