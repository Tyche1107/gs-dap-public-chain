#!/usr/bin/env python3
"""
Create shocking visualizations for Goldman Sachs GS DAP vs Public RWA analysis
"""

import json
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

# Load data
with open('data/public_rwa_analysis.json') as f:
    data = json.load(f)

# 1. Market Share Pie Chart - GS DAP vs Public RWA
fig, ax = plt.subplots(figsize=(10, 8))

total_market = data['public_rwa_tvl'] + data['gs_dap_tvl']
market_data = [data['public_rwa_tvl'], data['gs_dap_tvl']]
labels = [f'Public RWA\n(9+ Protocols)\n${data["public_rwa_tvl"]/1e9:.2f}B', 
          f'GS DAP\n(Canton)\n${data["gs_dap_tvl"]/1e6:.0f}M']
colors = ['#2ecc71', '#e74c3c']
explode = (0.05, 0.1)

wedges, texts, autotexts = ax.pie(market_data, labels=labels, autopct='%1.1f%%',
                                    colors=colors, startangle=90, explode=explode,
                                    textprops={'fontsize': 13, 'fontweight': 'bold'})

ax.set_title('RWA Market Distribution: Public vs Permissioned\nGS DAP Locked Out of 73% of Market',
             fontsize=14, fontweight='bold', pad=20)

# Add annotation
ax.annotate(f'{data["market_share_gap"]:.0f}% market\ninaccessible', 
            xy=(-0.5, 0.5), xytext=(-1.2, 0.2),
            arrowprops=dict(arrowstyle='->', color='red', lw=3),
            fontsize=14, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('charts/gs_dap_market_share.png', dpi=300, bbox_inches='tight')
print("✅ Created: charts/gs_dap_market_share.png")

# 2. Public RWA Protocols Breakdown - Who's Winning
fig, ax = plt.subplots(figsize=(12, 8))

protocols = list(data['tvl_estimates'].keys())
tvls = [data['tvl_estimates'][p] / 1e6 for p in protocols]  # Convert to millions

# Sort by TVL
sorted_data = sorted(zip(protocols, tvls), key=lambda x: x[1], reverse=True)
protocols_sorted = [x[0] for x in sorted_data]
tvls_sorted = [x[1] for x in sorted_data]

colors_bar = plt.cm.viridis(np.linspace(0.3, 0.9, len(protocols_sorted)))

bars = ax.barh(protocols_sorted, tvls_sorted, color=colors_bar, alpha=0.8, 
               edgecolor='black', linewidth=2)

# Add value labels
for bar, val in zip(bars, tvls_sorted):
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2,
            f' ${val:.0f}M',
            ha='left', va='center', fontsize=11, fontweight='bold')

ax.set_xlabel('Total Value Locked ($ Millions)', fontsize=13, fontweight='bold')
ax.set_title('Public RWA Ecosystem: $1.85B Across 9 Protocols\nGS DAP (Canton): $500M, 3 Clients Only',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add GS DAP comparison line
ax.axvline(x=500, color='red', linestyle='--', linewidth=3, label='GS DAP Total ($500M)')
ax.legend(fontsize=12, loc='lower right')

# Add annotation
ax.text(700, 7, 'GS DAP would rank\n#3 if public,\nbut locked out',
        fontsize=11, color='red', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('charts/public_rwa_breakdown.png', dpi=300, bbox_inches='tight')
print("✅ Created: charts/public_rwa_breakdown.png")

# 3. Client Count vs TVL - Capital Efficiency
fig, ax = plt.subplots(figsize=(10, 7))

# Sample data points (estimated client counts for public protocols)
protocols_scatter = ['Centrifuge', 'Maple', 'Ondo', 'Backed', 'Goldfinch', 'GS DAP']
tvls_scatter = [425, 380, 421, 180, 120, 500]
clients_scatter = [850, 420, 643, 320, 180, 3]  # Estimated for public, actual for GS DAP
colors_scatter = ['green', 'green', 'green', 'green', 'green', 'red']

scatter = ax.scatter(clients_scatter, tvls_scatter, s=[c*5 for c in clients_scatter], 
                     alpha=0.6, c=colors_scatter, edgecolors='black', linewidth=2)

# Add labels
for i, protocol in enumerate(protocols_scatter):
    ax.annotate(protocol, (clients_scatter[i], tvls_scatter[i]),
                xytext=(10, 10), textcoords='offset points',
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

ax.set_xlabel('Number of Clients/Users', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Value Locked ($ Millions)', fontsize=13, fontweight='bold')
ax.set_title('Capital Efficiency: Public RWA vs GS DAP\nGS DAP: Highest TVL per Client, Lowest Total Reach',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_xscale('log')

# Add efficiency line (TVL per client)
efficiency_line_x = np.array([1, 1000])
efficiency_line_y = efficiency_line_x * (500/3)  # GS DAP's efficiency
ax.plot(efficiency_line_x, efficiency_line_y, 'r--', alpha=0.5, linewidth=2,
        label=f'GS DAP Efficiency ($167M/client)')
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('charts/capital_efficiency.png', dpi=300, bbox_inches='tight')
print("✅ Created: charts/capital_efficiency.png")

# 4. Valuation Multiple Comparison
fig, ax = plt.subplots(figsize=(12, 7))

companies = ['Ondo\nFinance', 'GS DAP\n(Canton)', 'Centrifuge', 'Maple\nFinance']
multiples = [2.85, 1.00, 0.82, 0.74]
tvls_val = [421, 500, 425, 380]
colors_val = ['#2ecc71', '#e74c3c', '#3498db', '#9b59b6']

x_pos = np.arange(len(companies))
bars = ax.bar(x_pos, multiples, color=colors_val, alpha=0.8, 
              edgecolor='black', linewidth=2)

# Add TVL labels on bars
for i, (bar, tvl, mult) in enumerate(zip(bars, tvls_val, multiples)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{mult:.2f}x\n(TVL: ${tvl}M)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Valuation / TVL Multiple', fontsize=13, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(companies, fontsize=12, fontweight='bold')
ax.set_title('Valuation Multiples: Public RWA vs GS DAP\nOndo Premium (2.85x) vs GS DAP Fair Value (1.00x)',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Add average line
avg_public = np.mean([2.85, 0.82, 0.74])
ax.axhline(y=avg_public, color='green', linestyle='--', linewidth=2,
           label=f'Public RWA Avg ({avg_public:.2f}x)')
ax.legend(fontsize=11)

# Add annotation
ax.annotate('Permissionless\npremium', 
            xy=(0, 2.85), xytext=(0.5, 2.3),
            arrowprops=dict(arrowstyle='->', color='green', lw=2),
            fontsize=11, color='green', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('charts/valuation_multiples.png', dpi=300, bbox_inches='tight')
print("✅ Created: charts/valuation_multiples.png")

# 5. Strategic Decision Matrix
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

fig.suptitle('GS DAP Strategic Positioning: Wrong Platform for Growth', 
             fontsize=16, fontweight='bold', y=0.98)

# Create comparison table
dimensions = [
    {'metric': 'Total Addressable Market', 'public': '$1.85B', 'canton': '$500M', 'gap': '73% locked out'},
    {'metric': 'Client/Protocol Count', 'public': '9+ protocols', 'canton': '3 clients', 'gap': '75% fewer entities'},
    {'metric': 'DeFi Composability', 'public': 'Full integration', 'canton': 'None', 'gap': '100% gap'},
    {'metric': 'Developer Ecosystem', 'public': 'Open', 'canton': 'Closed', 'gap': 'Zero 3rd party'},
    {'metric': 'Network Effects', 'public': 'Strong', 'canton': 'Minimal', 'gap': 'Limited growth'},
    {'metric': 'Valuation Multiple', 'public': '1.47x avg', 'canton': '1.00x', 'gap': '32% discount'},
]

y_start = 0.85
for i, dim in enumerate(dimensions):
    y = y_start - i * 0.12
    
    # Metric name
    ax.text(0.05, y, dim['metric'], fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray'))
    
    # Public value (green)
    ax.text(0.35, y, dim['public'], fontsize=11, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', edgecolor='green', linewidth=2))
    
    # Canton value (red)
    ax.text(0.55, y, dim['canton'], fontsize=11, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', edgecolor='red', linewidth=2))
    
    # Gap
    ax.text(0.78, y, dim['gap'], fontsize=10, color='red', fontweight='bold')

# Column headers
ax.text(0.35, 0.92, 'Public RWA', fontsize=13, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen'))
ax.text(0.55, 0.92, 'GS DAP (Canton)', fontsize=13, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc'))

# Bottom recommendation
recommendation = ("STRATEGIC RECOMMENDATION:\nGS DAP optimized for ultra-large deals ($100M+), but public RWA captured broader market.\n"
                  "Either: (1) Accept niche positioning, or (2) Launch permissionless token for growth.")
ax.text(0.5, 0.08, recommendation, fontsize=11, ha='center', style='italic',
        bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', edgecolor='orange', linewidth=3))

plt.tight_layout()
plt.savefig('charts/strategic_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Created: charts/strategic_matrix.png")

print("\n✅ All GS DAP visualizations created successfully!")
print("📁 Saved to: charts/")
