# Fractal Visions Soneium Dune Pipeline 

Hello! This repository contains the ETL pipeline for <a href="https://dune.com/visionwizards/fractal-visions-soneium" target="_blank" rel="noopener noreferrer"> Fractal Visions Marketplace X Soneium Dune Dashboard</a>. 

The pipeline 
1. collects Fractal Visions Marketplace contract activity on the Soneium Chain using RPC API `0xF87f5313E830d8E2670898e231D8701532b1eB09` 
2. decodes transaction logs with a custom Python script
3. uploads the data onto Dune Analytics platform using SDK

## Stacks used
<b>Data Collection</b>: Python, Blockscout RPC API <br>
<b>Data Processing</b>: Python, Web3.py, eth-abi <br>
<b>Orchestration</b>: GitHub Actions <br>

GitHub Actions Workflow: pipeline runs every 6 hours. 

# Directory Structure  
      .
      ├── .github/workflows             # Defines orchestration 
      │   └──soneium-pipeline.yml
      ├── utils                         
      │   ├── create_tables.py          # Creates empty tables on Dune
      │   ├── event_decode.py           # Functions to decode Marketplace events
      │   └── topic_map.py              # Topic key mapping for the contract
      ├── initialize.py                 # Initializes first blocks to enable Dune-query-based ingestion checkpoints
      ├── ingest.py                     # Script to run incremental pipeline            
      └── requirements.txt              # Dependencies 

# Requirements 
- Python 3.11+
- Pandas 2.2.0
- Dune SDK 1.3.0
- Web3 6.0.0
- ETH-abi 4.0.0
- API Keys (Dune Analytics) <br>
