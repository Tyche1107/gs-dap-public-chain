#!/usr/bin/env python3
"""
Fetch BUIDL token holders from Etherscan API
"""
import requests
import json
import time
from typing import List, Dict

ETHERSCAN_API_KEY = "NPSPUHS61RHBNF49VJTZT23KE8PBV2PZ7A"
BUIDL_CONTRACT = "0x7712c34205737192402172409a8f7ccef8aa2aec"
BASE_URL = "https://api.etherscan.io/api"

def get_token_holders(contract_address: str, page: int = 1, offset: int = 100) -> Dict:
    """Get token holders from Etherscan"""
    params = {
        'module': 'token',
        'action': 'tokenholderlist',
        'contractaddress': contract_address,
        'page': page,
        'offset': offset,
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == '1':
        return data['result']
    else:
        print(f"Error: {data.get('message', 'Unknown error')}")
        return []

def get_total_supply(contract_address: str) -> int:
    """Get total supply of token"""
    params = {
        'module': 'stats',
        'action': 'tokensupply',
        'contractaddress': contract_address,
        'apikey': ETHERSCAN_API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if data['status'] == '1':
        return int(data['result'])
    return 0

def main():
    print(f"Fetching BUIDL token holders: {BUIDL_CONTRACT}")
    
    # Get total supply
    total_supply = get_total_supply(BUIDL_CONTRACT)
    print(f"Total supply: {total_supply / 10**6:,.2f} BUIDL")
    
    # Get all holders (fetch multiple pages if needed)
    all_holders = []
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        holders = get_token_holders(BUIDL_CONTRACT, page=page, offset=100)
        
        if not holders:
            break
            
        all_holders.extend(holders)
        
        if len(holders) < 100:  # Last page
            break
            
        page += 1
        time.sleep(0.3)  # Rate limiting
    
    print(f"\nTotal holders found: {len(all_holders)}")
    
    # Process and save
    processed_holders = []
    for holder in all_holders:
        processed_holders.append({
            'address': holder['TokenHolderAddress'].lower(),
            'balance': int(holder['TokenHolderQuantity']),
            'balance_readable': int(holder['TokenHolderQuantity']) / 10**6,
            'percentage': (int(holder['TokenHolderQuantity']) / total_supply * 100) if total_supply > 0 else 0
        })
    
    # Sort by balance
    processed_holders.sort(key=lambda x: x['balance'], reverse=True)
    
    # Save to file
    output = {
        'contract': BUIDL_CONTRACT,
        'total_supply': total_supply,
        'total_supply_readable': total_supply / 10**6,
        'holder_count': len(processed_holders),
        'fetch_timestamp': int(time.time()),
        'holders': processed_holders
    }
    
    with open('../data/buidl_holders.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nData saved to ../data/buidl_holders.json")
    
    # Print top 10
    print("\nTop 10 holders:")
    for i, holder in enumerate(processed_holders[:10], 1):
        print(f"{i:2d}. {holder['address']}: {holder['balance_readable']:>15,.2f} BUIDL ({holder['percentage']:.2f}%)")

if __name__ == '__main__':
    main()
