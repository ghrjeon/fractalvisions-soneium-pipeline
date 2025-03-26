import requests
import json
import os
from utils.event_decode import decode_NewListing, decode_NewSale, decode_CancelledListing, decode_NewOffer
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import dotenv
import time
from utils.topic_map import topic_mapping
import pandas as pd 

dotenv.load_dotenv()

dune = DuneClient(os.getenv("DUNE_API_KEY_FRACTALVISIONS_SONEIUM"))

def fetch_logs(instance_url, from_block, to_block, contract_address, topic0, max_retries=5, initial_delay=5):
    """
    Fetch logs from a blockchain node using RPC call with retry logic
    Args:
        instance_url (str): Base URL of the blockchain node
        max_retries (int): Maximum number of retry attempts
        initial_delay (int): Initial delay in seconds before retrying
    """
    url = instance_url
    params = {
        "module": "logs",
        "action": "getLogs",
        "fromBlock": from_block,
        "toBlock": to_block,
        "address": contract_address,
        "topic0": topic0
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            logs = response.json()
            
            # Check for rate limit error
            if logs.get("message") == "429 Too Many Requests":
                delay = initial_delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit hit. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}")
                time.sleep(delay)
                continue
                
            return logs
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Failed after {max_retries} attempts: {str(e)}")
                return None
            delay = initial_delay * (2 ** attempt)
            print(f"Request failed. Waiting {delay} seconds before retry {attempt + 1}/{max_retries}")
            time.sleep(delay)
    
    return None

def fetch_block_range(instance_url, from_block, to_block, contract_address, topic0, topic_name):
    """
    Fetch all logs from a blockchain node using RPC call with incremental saving
    """
    all_logs = []
    current_from = from_block
    highest_processed_block = from_block - 1
    print(f"Starting to fetch logs for {topic_name} from block {from_block} to {to_block}")

    # Create raw directory if it doesn't exist
    os.makedirs("raw", exist_ok=True)
    
    # Check for existing progress file
    progress_file = f"raw/{topic_name}_progress.json"
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            progress_data = json.load(f)
            all_logs = progress_data.get('logs', [])
            current_from = progress_data.get('last_processed_block', from_block)
            highest_processed_block = progress_data.get('highest_processed_block', from_block - 1)
            print(f"Resuming from block {current_from} with {len(all_logs)} existing logs")

    while True:
        print(f"Fetching batch starting from block {current_from}")

        current_from = str(current_from)
        to_block = str(to_block)
        result = fetch_logs(instance_url, current_from, to_block, contract_address, topic0)
        
        if not result:
            print("Failed to fetch logs after all retries")
            break
            
        if 'result' not in result:
            print(f"Unexpected API response structure: {result}")
            break
            
        batch_logs = result['result']
        if not isinstance(batch_logs, list):
            print(f"Unexpected batch_logs type: {type(batch_logs)}")
            break
            
        batch_size = len(batch_logs)
        print(f"Retrieved {batch_size} logs in this batch")
        
        if batch_size == 0:
            break
                
        all_logs.extend(batch_logs)
        
        # Save progress after each successful batch
        progress_data = {
            'logs': all_logs,
            'last_processed_block': current_from,
            'highest_processed_block': highest_processed_block
        }
        with open(progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
        print(f"Saved progress: {len(all_logs)} logs so far")
        
        if batch_size < 1000:
            if batch_logs:
                block_numbers = [int(log.get('blockNumber', '0x0'), 16) for log in batch_logs]
                if block_numbers:
                    highest_processed_block = max(max(block_numbers), highest_processed_block)
            break
        
        if batch_logs:
            block_numbers = [int(log.get('blockNumber', '0x0'), 16) for log in batch_logs]
            if block_numbers:
                max_block = max(block_numbers)
                highest_processed_block = max(max_block, highest_processed_block)
                current_from = max_block + 1
                print(f"Continuing from block {current_from}")
                time.sleep(5)
            else:
                break
    
    print(f"Total logs fetched: {len(all_logs)} with highest block {highest_processed_block}")
    
    # Remove duplicates
    unique_dict = {(log['transactionHash']): log for log in all_logs}
    all_logs = list(unique_dict.values())
    
    # Save final results
    output_file = f"raw/{topic_name}_initial.json"
    with open(output_file, "w") as f:
        json.dump(all_logs, f, indent=2)
    
    # Clean up progress file
    if os.path.exists(progress_file):
        os.remove(progress_file)
        
    return all_logs



def main():
    try:
        instance_url = "https://soneium.blockscout.com/api"
        contract_address = "0xF87f5313E830d8E2670898e231D8701532b1eB09"
        from_block = 1871690
        to_block = 3500000
        decoder_functions = {
            "NewSale": decode_NewSale,
            "NewListing": decode_NewListing,
            "CancelledListing": decode_CancelledListing,
            "NewOffer": decode_NewOffer
        }
     
        for topic in topic_mapping:
            try:
                topic0 = topic["topic0"]
                topic_name = topic["event_type"]
                table_name = topic["table_name"]
                decoder = decoder_functions[topic_name]
                print(f"\nProcessing {topic_name} on {table_name} with {decoder}")

                print(f"Fetching logs from block {from_block} to {to_block}")

                all_logs = fetch_block_range(
                    instance_url,
                    from_block,
                    to_block,
                    contract_address,
                    topic0,
                    topic_name
                )

                print(f"Fetched {len(all_logs)} logs")

                # Create decoded directory if it doesn't exist
                os.makedirs("decoded", exist_ok=True)

                # Decode the logs and save to a csv file
                df = decoder(all_logs)
                print(f"Decoded {len(df)} logs")
                
                df['event_type'] = topic_name

                # save to a csv file
                df.to_csv(f"decoded/{topic_name}_initial.csv", index=False)
                
                # upload to dune
                with open(f"decoded/{topic_name}_initial.csv", "rb") as data:
                    response = dune.insert_table(
                            namespace="visionwizards",
                            table_name=f"{table_name}",
                            data=data,
                            content_type="text/csv"
                        )

                print(f"Uploaded {len(df)} logs to dune")
                print(response)
                
            except Exception as e:
                print(f"Error processing topic {topic_name}: {str(e)}")
                continue  # Continue with next topic even if one fails
                
    except Exception as e:
        print(f"Fatal error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()