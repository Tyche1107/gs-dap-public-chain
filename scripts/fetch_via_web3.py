#!/usr/bin/env python3
"""
Fetch BUIDL data using web3.py and public RPC
"""
import json
import time
from web3 import Web3
from collections import defaultdict

# Public RPC endpoints
RPC_URL = "https://eth.llamarpc.com"  # Public endpoint

BUIDL_CONTRACT = "0x7712c34205737192402172409a8f7ccef8aa2aec"

# ERC20 ABI (minimal - just what we need)
ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

def main():
    print("Connecting to Ethereum via Web3...")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print("Failed to connect to Ethereum network")
        return
    
    print(f"Connected! Latest block: {w3.eth.block_number}\n")
    
    # Create contract instance
    contract = w3.eth.contract(address=Web3.to_checksum_address(BUIDL_CONTRACT), abi=ERC20_ABI)
    
    # Get token info
    print("Fetching token information...")
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        
        print(f"Token: {name} ({symbol})")
        print(f"Decimals: {decimals}")
        print(f"Total Supply: {total_supply / 10**decimals:,.2f} {symbol}\n")
    except Exception as e:
        print(f"Error fetching token info: {e}")
        decimals = 6  # Default assumption
        total_supply = 0
    
    # Get Transfer events to find all holders
    print("Fetching Transfer events...")
    
    # Get contract creation block (approximate - BUIDL launched in March 2024)
    # Block 19400000 is around March 20, 2024
    start_block = 19400000
    current_block = w3.eth.block_number
    
    # Fetch in chunks to avoid timeout
    chunk_size = 10000
    all_addresses = set()
    
    transfer_event_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()
    
    print(f"Scanning blocks {start_block} to {current_block}...")
    
    for block_start in range(start_block, current_block + 1, chunk_size):
        block_end = min(block_start + chunk_size - 1, current_block)
        print(f"Blocks {block_start:,} - {block_end:,}...", end='\r')
        
        try:
            logs = w3.eth.get_logs({
                'address': Web3.to_checksum_address(BUIDL_CONTRACT),
                'fromBlock': block_start,
                'toBlock': block_end,
                'topics': [transfer_event_signature]
            })
            
            for log in logs:
                # Extract from and to addresses from topics
                if len(log['topics']) >= 3:
                    from_addr = Web3.to_checksum_address('0x' + log['topics'][1].hex()[-40:])
                    to_addr = Web3.to_checksum_address('0x' + log['topics'][2].hex()[-40:])
                    
                    if from_addr != '0x0000000000000000000000000000000000000000':
                        all_addresses.add(from_addr)
                    if to_addr != '0x0000000000000000000000000000000000000000':
                        all_addresses.add(to_addr)
            
            time.sleep(0.1)  # Rate limiting
            
        except Exception as e:
            print(f"\nError fetching logs for blocks {block_start}-{block_end}: {e}")
            continue
    
    print(f"\nFound {len(all_addresses)} unique addresses")
    
    # Query current balance for each address
    print("\nQuerying current balances...")
    holders = []
    
    for i, address in enumerate(all_addresses, 1):
        print(f"Querying {i}/{len(all_addresses)}: {address}...", end='\r')
        
        try:
            balance = contract.functions.balanceOf(address).call()
            
            if balance > 0:
                holders.append({
                    'address': address.lower(),
                    'balance': balance,
                    'balance_readable': balance / 10**decimals
                })
        except Exception as e:
            print(f"\nError querying balance for {address}: {e}")
            continue
    
    print(f"\n\nFound {len(holders)} holders with non-zero balance")
    
    # Sort by balance
    holders.sort(key=lambda x: x['balance'], reverse=True)
    
    # Calculate actual total from holders
    actual_total = sum(h['balance'] for h in holders)
    
    # Calculate percentages
    for holder in holders:
        holder['percentage'] = (holder['balance'] / actual_total * 100) if actual_total > 0 else 0
    
    # Save to file
    output = {
        'contract': BUIDL_CONTRACT.lower(),
        'total_supply': actual_total,
        'total_supply_readable': actual_total / 10**decimals,
        'decimals': decimals,
        'holder_count': len(holders),
        'fetch_timestamp': int(time.time()),
        'holders': holders
    }
    
    with open('../data/buidl_holders.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nData saved to ../data/buidl_holders.json")
    
    # Print top 20
    print("\nTop 20 holders:")
    for i, holder in enumerate(holders[:20], 1):
        print(f"{i:2d}. {holder['address']}: {holder['balance_readable']:>15,.2f} ({holder['percentage']:.2f}%)")

if __name__ == '__main__':
    main()
