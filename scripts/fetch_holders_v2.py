#!/usr/bin/env python3
"""
Fetch BUIDL token holders using contract balance queries
Alternative method when tokenholderlist API is unavailable
"""
import requests
import json
import time
from typing import List, Dict, Set

ETHERSCAN_API_KEY = "NPSPUHS61RHBNF49VJTZT23KE8PBV2PZ7A"
BUIDL_CONTRACT = "0x7712c34205737192402172409a8f7ccef8aa2aec"
BASE_URL = "https://api.etherscan.io/api"

def get_contract_info():
    """Get basic contract info"""
    params = {
        'module': 'contract',
        'action': 'getsourcecode',
        'address': BUIDL_CONTRACT,
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print("Contract info:", json.dumps(data, indent=2))
    return data

def get_transfer_events(start_block: int = 0, end_block: int = 99999999) -> List[Dict]:
    """Get Transfer events from contract"""
    params = {
        'module': 'logs',
        'action': 'getLogs',
        'address': BUIDL_CONTRACT,
        'fromBlock': start_block,
        'toBlock': end_block,
        'topic0': '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',  # Transfer event
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == '1':
        return data['result']
    else:
        print(f"Error getting transfers: {data.get('message', 'Unknown error')}")
        return []

def get_token_balance(contract_address: str, holder_address: str) -> int:
    """Get token balance for a specific holder"""
    params = {
        'module': 'account',
        'action': 'tokenbalance',
        'contractaddress': contract_address,
        'address': holder_address,
        'tag': 'latest',
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == '1':
        return int(data['result'])
    return 0

def main():
    print(f"Analyzing BUIDL contract: {BUIDL_CONTRACT}\n")
    
    # First, get contract info
    print("Step 1: Getting contract information...")
    contract_info = get_contract_info()
    time.sleep(0.3)
    
    # Get all transfer events to identify holders
    print("\nStep 2: Fetching Transfer events...")
    transfers = get_transfer_events()
    print(f"Found {len(transfers)} transfer events")
    
    # Extract unique addresses
    unique_addresses: Set[str] = set()
    for transfer in transfers:
        # Transfer event topics: [0] = signature, [1] = from, [2] = to
        if len(transfer.get('topics', [])) >= 3:
            from_addr = '0x' + transfer['topics'][1][-40:]
            to_addr = '0x' + transfer['topics'][2][-40:]
            
            if from_addr != '0x0000000000000000000000000000000000000000':
                unique_addresses.add(from_addr.lower())
            if to_addr != '0x0000000000000000000000000000000000000000':
                unique_addresses.add(to_addr.lower())
    
    print(f"Found {len(unique_addresses)} unique addresses involved in transfers")
    
    # Query current balance for each address
    print("\nStep 3: Querying current balances...")
    holders = []
    total_supply = 0
    
    for i, address in enumerate(unique_addresses, 1):
        print(f"Querying {i}/{len(unique_addresses)}: {address}...", end='\r')
        balance = get_token_balance(BUIDL_CONTRACT, address)
        
        if balance > 0:
            holders.append({
                'address': address,
                'balance': balance,
                'balance_readable': balance / 10**6  # Assuming 6 decimals
            })
            total_supply += balance
        
        time.sleep(0.25)  # Rate limiting
    
    print(f"\nFound {len(holders)} holders with non-zero balance")
    print(f"Total supply: {total_supply / 10**6:,.2f} BUIDL")
    
    # Sort by balance
    holders.sort(key=lambda x: x['balance'], reverse=True)
    
    # Calculate percentages
    for holder in holders:
        holder['percentage'] = (holder['balance'] / total_supply * 100) if total_supply > 0 else 0
    
    # Save to file
    output = {
        'contract': BUIDL_CONTRACT,
        'total_supply': total_supply,
        'total_supply_readable': total_supply / 10**6,
        'holder_count': len(holders),
        'fetch_timestamp': int(time.time()),
        'holders': holders
    }
    
    with open('../data/buidl_holders.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nData saved to ../data/buidl_holders.json")
    
    # Print top 10
    print("\nTop 10 holders:")
    for i, holder in enumerate(holders[:10], 1):
        print(f"{i:2d}. {holder['address']}: {holder['balance_readable']:>15,.2f} BUIDL ({holder['percentage']:.2f}%)")

if __name__ == '__main__':
    main()
