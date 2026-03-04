#!/usr/bin/env python3
"""
Generate professional figures for GS DAP report
"""
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import numpy as np

# Professional styling
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
rcParams['font.size'] = 10
rcParams['axes.labelsize'] = 11
rcParams['axes.titlesize'] = 12
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9
rcParams['figure.titlesize'] = 13

# Color palette (professional, colorblind-friendly)
COLORS = {
    'primary': '#2E5C8A',      # Blue - institutional
    'defi': '#E8743B',          # Orange - DeFi active
    'cross_chain': '#53A567',   # Green - cross-chain
    'hold': '#8C8C8C',          # Gray - hold only
    'risk_high': '#C84547',     # Red
    'risk_medium': '#E8A838',   # Yellow
    'risk_low': '#5B9A68'       # Green
}

def load_analysis():
    """Load analysis results"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_path = os.path.join(script_dir, '..', 'analysis', 'full_analysis.json')
    with open(analysis_path, 'r') as f:
        return json.load(f)

def figure_1_behavior_distribution(analysis):
    """
    Figure 1: Asset Distribution by Behavior Type
    Stacked bar showing hold vs DeFi vs cross-chain
    """
    behavior = analysis['behavior_analysis']
    
    categories = ['Hold Only', 'DeFi Active', 'Cross-Chain']
    values = [
        behavior['hold_only']['value_usd'] / 1e6,  # Convert to millions
        behavior['defi_active']['value_usd'] / 1e6,
        behavior['cross_chain']['value_usd'] / 1e6
    ]
    percentages = [
        behavior['hold_only']['percentage'],
        behavior['defi_active']['percentage'],
        behavior['cross_chain']['percentage']
    ]
    colors = [COLORS['hold'], COLORS['defi'], COLORS['cross_chain']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Horizontal stacked bar
    left = 0
    for i, (cat, val, pct, color) in enumerate(zip(categories, values, percentages, colors)):
        ax.barh(0, val, left=left, color=color, edgecolor='white', linewidth=2, height=0.6)
        
        # Add percentage label
        label_x = left + val/2
        ax.text(label_x, 0, f'{cat}\n${val:.1f}M\n({pct:.1f}%)', 
                ha='center', va='center', fontweight='bold', fontsize=11, color='white')
        
        left += val
    
    ax.set_xlim(0, analysis['total_value_usd'] / 1e6)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel('Assets Under Management ($ millions)', fontweight='bold')
    ax.set_title('BUIDL Asset Distribution by Holder Behavior\n56 holders, $171.8M total', 
                 fontweight='bold', pad=20)
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add key finding box
    finding_text = f"32% of assets self-selected DeFi/cross-chain utility"
    ax.text(0.5, -0.35, finding_text, transform=ax.transAxes,
            fontsize=12, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF8DC', edgecolor=COLORS['primary'], linewidth=2))
    
    plt.tight_layout()
    plt.savefig('fig1_behavior_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 1: Behavior distribution saved")
    plt.close()

def figure_2_counterparty_credibility(analysis):
    """
    Figure 2: DeFi Counterparty Credibility Scores
    Bar chart of credibility by protocol
    """
    cp_data = analysis['counterparty_analysis']['by_protocol']
    
    protocols = list(cp_data.keys())
    credibility = [cp_data[p]['credibility_score'] for p in protocols]
    sybil_rates = [cp_data[p]['sybil_rate'] for p in protocols]
    
    # Sort by credibility descending
    sorted_data = sorted(zip(protocols, credibility, sybil_rates), key=lambda x: x[1], reverse=True)
    protocols, credibility, sybil_rates = zip(*sorted_data)
    
    # Color by risk level
    colors_list = []
    for p in protocols:
        risk = cp_data[p]['risk_level']
        if risk == 'very_low' or risk == 'low':
            colors_list.append(COLORS['risk_low'])
        elif risk == 'medium':
            colors_list.append(COLORS['risk_medium'])
        else:
            colors_list.append(COLORS['risk_high'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = np.arange(len(protocols))
    bars = ax.barh(y_pos, credibility, color=colors_list, edgecolor='white', linewidth=1.5)
    
    # Add percentage labels
    for i, (bar, cred, sybil) in enumerate(zip(bars, credibility, sybil_rates)):
        ax.text(bar.get_width() - 3, bar.get_y() + bar.get_height()/2,
                f'{cred:.1f}%\n({sybil:.1f}% sybil)',
                ha='right', va='center', fontweight='bold', fontsize=9, color='white')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([p.replace('_', ' ').title() for p in protocols])
    ax.set_xlabel('Credibility Score (%)', fontweight='bold')
    ax.set_title('DeFi Counterparty Credibility Assessment\nBased on sybil detection analysis',
                 fontweight='bold', pad=15)
    ax.set_xlim(0, 100)
    ax.axvline(90, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(90, -0.5, '90% threshold', fontsize=8, ha='center', color='gray')
    
    # Legend
    legend_elements = [
        mpatches.Patch(color=COLORS['risk_low'], label='Low/Very Low Risk'),
        mpatches.Patch(color=COLORS['risk_medium'], label='Medium Risk'),
        mpatches.Patch(color=COLORS['risk_high'], label='High Risk')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('fig2_counterparty_credibility.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 2: Counterparty credibility saved")
    plt.close()

def figure_3_permission_boundary(analysis):
    """
    Figure 3: Permission Boundary Efficacy
    Pie chart showing where assets went
    """
    boundary = analysis['boundary_analysis']['boundary_events']
    
    categories = [
        'Hold in Custody',
        'DeFi on Ethereum',
        'Cross-Chain Migration'
    ]
    values = [
        boundary['expected_behavior']['hold_in_custody'],
        boundary['semi_expected']['defi_on_ethereum'],
        boundary['boundary_crossing']['cross_chain_migration']
    ]
    colors = [COLORS['hold'], COLORS['defi'], COLORS['cross_chain']]
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Pie chart with explosion
    explode = (0, 0.05, 0.1)
    wedges, texts, autotexts = ax.pie(values, explode=explode, labels=categories,
                                        colors=colors, autopct='%1.1f%%',
                                        startangle=90, textprops={'fontweight': 'bold', 'fontsize': 11})
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('Permission Boundary Efficacy: Where Did Whitelisted Assets Go?\n56 holders, Ethereum-based whitelist',
                 fontweight='bold', pad=20, fontsize=13)
    
    # Add finding box
    finding = f"85.7% stayed on Ethereum\n14.3% crossed to other chains"
    ax.text(0.5, -0.15, finding, transform=ax.transAxes,
            fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF8DC', edgecolor=COLORS['primary'], linewidth=2))
    
    plt.tight_layout()
    plt.savefig('fig3_permission_boundary.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 3: Permission boundary saved")
    plt.close()

def figure_4_strategic_summary(analysis):
    """
    Figure 4: Strategic Summary Dashboard
    Key metrics for GS DAP decision makers
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('BUIDL On-Chain Behavior: Strategic Summary for GS DAP', 
                 fontweight='bold', fontsize=14, y=0.98)
    
    # Metric 1: Organic DeFi %
    ax1.text(0.5, 0.6, '32.0%', ha='center', va='center',
             fontsize=48, fontweight='bold', color=COLORS['defi'])
    ax1.text(0.5, 0.3, 'of assets entered DeFi\norganically', ha='center', va='center',
             fontsize=12, fontweight='bold')
    ax1.text(0.5, 0.1, '$54.9M self-selected DeFi utility', ha='center', va='center',
             fontsize=10, style='italic')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, 
                                 edgecolor=COLORS['defi'], linewidth=3))
    
    # Metric 2: Counterparty Credibility
    ax2.text(0.5, 0.6, '89.7%', ha='center', va='center',
             fontsize=48, fontweight='bold', color=COLORS['risk_low'])
    ax2.text(0.5, 0.3, 'average counterparty\ncredibility score', ha='center', va='center',
             fontsize=12, fontweight='bold')
    ax2.text(0.5, 0.1, '626 unique DeFi counterparties', ha='center', va='center',
             fontsize=10, style='italic')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                                 edgecolor=COLORS['risk_low'], linewidth=3))
    
    # Metric 3: Ethereum Retention
    ax3.text(0.5, 0.6, '85.7%', ha='center', va='center',
             fontsize=48, fontweight='bold', color=COLORS['primary'])
    ax3.text(0.5, 0.3, 'stayed on Ethereum\n(whitelist retention)', ha='center', va='center',
             fontsize=12, fontweight='bold')
    ax3.text(0.5, 0.1, '14.3% migrated cross-chain', ha='center', va='center',
             fontsize=10, style='italic')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis('off')
    ax3.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                                 edgecolor=COLORS['primary'], linewidth=3))
    
    # Metric 4: Holder Count & AUM
    ax4.text(0.5, 0.6, '56', ha='center', va='center',
             fontsize=48, fontweight='bold', color=COLORS['hold'])
    ax4.text(0.5, 0.3, 'unique holders\n$171.8M AUM', ha='center', va='center',
             fontsize=12, fontweight='bold')
    ax4.text(0.5, 0.1, 'As of March 3, 2026', ha='center', va='center',
             fontsize=10, style='italic')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False,
                                 edgecolor=COLORS['hold'], linewidth=3))
    
    plt.tight_layout()
    plt.savefig('fig4_strategic_summary.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 4: Strategic summary saved")
    plt.close()

def main():
    import os
    
    print("Generating figures for GS DAP report...\n")
    
    # Install matplotlib if needed
    try:
        import matplotlib
    except ImportError:
        print("Installing matplotlib...")
        import subprocess
        subprocess.run(['pip', 'install', 'matplotlib'], check=True)
    
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    figures_dir = os.path.join(script_dir, '..', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # Change to figures directory for saving
    os.chdir(figures_dir)
    
    analysis = load_analysis()
    
    figure_1_behavior_distribution(analysis)
    figure_2_counterparty_credibility(analysis)
    figure_3_permission_boundary(analysis)
    figure_4_strategic_summary(analysis)
    
    print("\n✓ All figures generated successfully!")
    print(f"  Output: {figures_dir}")

if __name__ == '__main__':
    main()
