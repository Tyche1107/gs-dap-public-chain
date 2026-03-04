#!/usr/bin/env python3
"""
Generate PDF report for GS DAP using ReportLab
"""
import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, 
                                PageBreak, Table, TableStyle, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def load_analysis():
    """Load analysis data"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, '..', 'analysis', 'full_analysis.json'), 'r') as f:
        return json.load(f)

def create_custom_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E5C8A'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2E5C8A'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='KeyFinding',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        leftIndent=20
    ))
    
    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='BulletPoint',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        leftIndent=30,
        fontName='Helvetica'
    ))
    
    return styles

def build_report(analysis):
    """Build the complete report"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(script_dir, '..', 'report', 
                               'GS_DAP_Public_Chain_Strategy_Report.pdf')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    doc = SimpleDocTemplate(report_path, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=1*inch, rightMargin=1*inch)
    
    story = []
    styles = create_custom_styles()
    
    # Cover page
    story.extend(build_cover_page(analysis, styles))
    story.append(PageBreak())
    
    # Executive Summary
    story.extend(build_executive_summary(analysis, styles))
    story.append(PageBreak())
    
    # Section 1: Organic DeFi Demand
    story.extend(build_section_organic_defi(analysis, styles, script_dir))
    story.append(PageBreak())
    
    # Section 2: Counterparty Credibility
    story.extend(build_section_counterparty(analysis, styles, script_dir))
    story.append(PageBreak())
    
    # Section 3: Permission Boundary
    story.extend(build_section_permission(analysis, styles, script_dir))
    story.append(PageBreak())
    
    # Strategic Implications
    story.extend(build_strategic_implications(analysis, styles, script_dir))
    
    # Build PDF
    doc.build(story)
    return report_path

def build_cover_page(analysis, styles):
    """Build cover page"""
    elements = []
    
    elements.append(Spacer(1, 1.5*inch))
    
    # Title with key metric
    title_text = f"{analysis['key_metric']['title_value']} of BlackRock BUIDL's Assets<br/>Entered DeFi Without Anyone Pushing.<br/>What This Tells GS DAP."
    elements.append(Paragraph(title_text, styles['CustomTitle']))
    
    elements.append(Spacer(1, 0.3*inch))
    
    # Subtitle (Chinese)
    subtitle_text = f"《贝莱德BUIDL有{analysis['key_metric']['title_value']}的资产自发进入了DeFi，<br/>这告诉了GS DAP什么》"
    elements.append(Paragraph(subtitle_text, styles['CustomSubtitle']))
    
    elements.append(Spacer(1, 1*inch))
    
    # Report info
    info_style = ParagraphStyle(
        'ReportInfo',
        parent=styles['ReportBody'],
        alignment=TA_CENTER,
        fontSize=10
    )
    
    elements.append(Paragraph("<b>Decision Support Analysis for Goldman Sachs Digital Asset Platform</b>", info_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("University of Washington | Decentralized Computing Lab", info_style))
    elements.append(Paragraph("Principal Investigator: Prof. Wei Cai", info_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"March 3, 2026", info_style))
    
    return elements

def build_executive_summary(analysis, styles):
    """Build executive summary"""
    elements = []
    
    elements.append(Paragraph("Executive Summary", styles['SectionHeading']))
    elements.append(Spacer(1, 0.1*inch))
    
    summary_text = """
    Goldman Sachs Digital Asset Platform (GS DAP) faces a strategic decision regarding public chain integration 
    following its November 2024 independence announcement. Private chain architectures cannot observe what 
    institutional clients do with tokenized assets once deployed to public chains. BlackRock's BUIDL token 
    provides the only mature case study of institutional tokenized assets operating on public Ethereum with 
    DeFi integration. This analysis examines 56 BUIDL holders ($171.8M AUM) to inform GS DAP's strategic 
    framework.
    """
    elements.append(Paragraph(summary_text.strip(), styles['ReportBody']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Key findings box
    findings_data = [
        ['<b>Key Finding</b>', '<b>Metric</b>', '<b>Implication</b>'],
        ['Organic DeFi Demand', 
         f"{analysis['key_metric']['title_value']} of assets",
         'Measurable client appetite for DeFi utility beyond custody'],
        ['Counterparty Credibility',
         f"{analysis['counterparty_analysis']['summary']['average_credibility_score']:.1f}% average score",
         'Established protocols show institutional-grade quality'],
        ['Permission Boundary',
         f"{analysis['boundary_analysis']['permission_scope']['ethereum_retention_rate']:.1f}% Ethereum retention",
         'Whitelist controls location, not interaction depth']
    ]
    
    findings_table = Table(findings_data, colWidths=[2*inch, 1.8*inch, 2.7*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5C8A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(findings_table)
    elements.append(Spacer(1, 0.2*inch))
    
    conclusion_text = """
    <b>Conclusion:</b> If GS DAP enables public chain deployment, expect similar organic DeFi engagement 
    (~30-35% of assets). Decision framework should incorporate counterparty risk surveillance, cross-chain 
    leakage mitigation, and regulatory perimeter management. This methodology scales to ongoing monitoring 
    of any tokenized asset on public chains.
    """
    elements.append(Paragraph(conclusion_text, styles['ReportBody']))
    
    return elements

def build_section_organic_defi(analysis, styles, script_dir):
    """Section 1: Organic DeFi Demand"""
    elements = []
    
    elements.append(Paragraph("1. Organic DeFi Demand: Client-Driven Utility Seeking", styles['SectionHeading']))
    
    behavior = analysis['behavior_analysis']
    
    text = f"""
    Analysis of BUIDL's 56 holders reveals that <b>{behavior['organic_defi_total']['percentage']:.1f}% 
    (${behavior['organic_defi_total']['value_usd']/1e6:.1f}M)</b> of assets self-selected DeFi or cross-chain 
    deployment <i>without issuer direction</i>. This represents measurable, organic demand for yield generation, 
    liquidity provision, and cross-chain utility.
    """
    elements.append(Paragraph(text.strip(), styles['ReportBody']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Breakdown
    breakdown_data = [
        ['<b>Behavior Type</b>', '<b>Addresses</b>', '<b>Value ($ millions)</b>', '<b>% of Total</b>'],
        ['Hold in Custody Only',
         str(behavior['hold_only']['count']),
         f"${behavior['hold_only']['value_usd']/1e6:.1f}",
         f"{behavior['hold_only']['percentage']:.1f}%"],
        ['DeFi Active (Ethereum)',
         str(behavior['defi_active']['count']),
         f"${behavior['defi_active']['value_usd']/1e6:.1f}",
         f"{behavior['defi_active']['percentage']:.1f}%"],
        ['Cross-Chain Migration',
         str(behavior['cross_chain']['count']),
         f"${behavior['cross_chain']['value_usd']/1e6:.1f}",
         f"{behavior['cross_chain']['percentage']:.1f}%"]
    ]
    
    breakdown_table = Table(breakdown_data, colWidths=[2.2*inch, 1.2*inch, 1.8*inch, 1.3*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8743B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(breakdown_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Add figure
    fig_path = os.path.join(script_dir, '..', 'figures', 'fig1_behavior_distribution.png')
    if os.path.exists(fig_path):
        img = Image(fig_path, width=6.5*inch, height=3.9*inch)
        elements.append(img)
    
    elements.append(Spacer(1, 0.1*inch))
    
    implication = """
    <b>Implication for GS DAP:</b> Institutional clients demonstrate measurable appetite for DeFi efficiency 
    beyond static custody. Permissioned architecture should accommodate—not block—this demand. Expect 
    30-35% of GS DAP assets to seek DeFi utility if public chain deployment is enabled.
    """
    elements.append(Paragraph(implication, styles['ReportBody']))
    
    return elements

def build_section_counterparty(analysis, styles, script_dir):
    """Section 2: Counterparty Credibility"""
    elements = []
    
    elements.append(Paragraph("2. DeFi Counterparty Credibility: Sybil Detection Analysis", 
                             styles['SectionHeading']))
    
    cp = analysis['counterparty_analysis']
    
    text = f"""
    Sybil detection analysis of {cp['summary']['total_unique_counterparties']} DeFi counterparties 
    across major protocols reveals <b>{cp['summary']['average_credibility_score']:.1f}% average credibility</b>. 
    Established protocols (Aave, Curve, Morpho) demonstrate institutional-grade counterparty quality with 
    <4% sybil rates. Newer market-making venues (UniswapX) show elevated clustering requiring additional 
    due diligence.
    """
    elements.append(Paragraph(text.strip(), styles['ReportBody']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Add figure
    fig_path = os.path.join(script_dir, '..', 'figures', 'fig2_counterparty_credibility.png')
    if os.path.exists(fig_path):
        img = Image(fig_path, width=6.5*inch, height=3.9*inch)
        elements.append(img)
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Key findings
    elements.append(Paragraph("<b>Key Findings:</b>", styles['KeyFinding']))
    for finding in cp['key_findings']:
        elements.append(Paragraph(f"• {finding}", styles['BulletPoint']))
    
    elements.append(Spacer(1, 0.1*inch))
    
    implication = """
    <b>Implication for GS DAP:</b> Counterparty risk is quantifiable and manageable. Established DeFi 
    protocols show institutional-grade credibility. However, ongoing surveillance is required—newer venues 
    may have elevated sybil clustering. This methodology enables continuous monitoring.
    """
    elements.append(Paragraph(implication, styles['ReportBody']))
    
    return elements

def build_section_permission(analysis, styles, script_dir):
    """Section 3: Permission Boundary Efficacy"""
    elements = []
    
    elements.append(Paragraph("3. Permission Boundary Efficacy: Whitelist Control Scope", 
                             styles['SectionHeading']))
    
    boundary = analysis['boundary_analysis']
    
    text = f"""
    Whitelist mechanisms retained <b>{boundary['permission_scope']['ethereum_retention_rate']:.1f}%</b> 
    of BUIDL assets on Ethereum mainnet. However, {boundary['boundary_events']['boundary_crossing']['percentage']:.1f}% 
    crossed to other chains (some with weaker regulatory frameworks), and {boundary['permission_scope']['defi_engagement_rate']:.1f}% 
    engaged DeFi protocols while remaining whitelisted. <i>Permissioning controls location but not interaction depth.</i>
    """
    elements.append(Paragraph(text.strip(), styles['ReportBody']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Add figure
    fig_path = os.path.join(script_dir, '..', 'figures', 'fig3_permission_boundary.png')
    if os.path.exists(fig_path):
        img = Image(fig_path, width=6.5*inch, height=4.2*inch)
        elements.append(img)
    
    elements.append(Spacer(1, 0.1*inch))
    
    # Key findings
    elements.append(Paragraph("<b>Key Findings:</b>", styles['KeyFinding']))
    for finding in boundary['key_findings']:
        elements.append(Paragraph(f"• {finding}", styles['BulletPoint']))
    
    elements.append(Spacer(1, 0.1*inch))
    
    implication = """
    <b>Implication for GS DAP:</b> Whitelisting provides geographic retention (85.7% stayed on Ethereum) 
    but limited control over DeFi interaction depth or cross-chain migration. If GS DAP enables public chain 
    deployment, expect ~15% cross-chain leakage and 20-30% DeFi engagement. Regulatory perimeter becomes 
    porous once assets are tokenized on public chains.
    """
    elements.append(Paragraph(implication, styles['ReportBody']))
    
    return elements

def build_strategic_implications(analysis, styles, script_dir):
    """Strategic implications for GS DAP"""
    elements = []
    
    elements.append(Paragraph("Strategic Implications for GS DAP", styles['SectionHeading']))
    
    # Summary figure
    fig_path = os.path.join(script_dir, '..', 'figures', 'fig4_strategic_summary.png')
    if os.path.exists(fig_path):
        img = Image(fig_path, width=6.5*inch, height=4.3*inch)
        elements.append(img)
    
    elements.append(Spacer(1, 0.15*inch))
    
    insights = analysis['strategic_insights']
    
    for i, insight in enumerate(insights, 1):
        elements.append(Paragraph(f"<b>{i}. {insight['finding']}</b>", styles['KeyFinding']))
        elements.append(Paragraph(insight['implication_for_gs_dap'], styles['ReportBody']))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Closing hook
    closing = """
    <b>Methodological Note:</b> This analysis is based on the BUIDL single case study, the only mature 
    example of institutional tokenized assets operating on public Ethereum with DeFi integration. The methodology—combining 
    on-chain behavior classification, sybil detection, and permission boundary analysis—scales to ongoing monitoring 
    of <i>any</i> tokenized asset on public chains. As GS DAP evaluates public chain strategy, this framework enables 
    data-driven assessment of counterparty risk, regulatory perimeter integrity, and organic client demand signals.
    """
    elements.append(Paragraph(closing.strip(), styles['ReportBody']))
    
    return elements

def main():
    print("Generating PDF report...\n")
    
    # Install reportlab if needed
    try:
        import reportlab
    except ImportError:
        print("Installing reportlab...")
        import subprocess
        subprocess.run(['pip', 'install', 'reportlab'], check=True, capture_output=True)
    
    analysis = load_analysis()
    report_path = build_report(analysis)
    
    print(f"✓ Report generated successfully!")
    print(f"  Output: {report_path}")
    print(f"\nTitle: {analysis['key_metric']['title_value']} of BlackRock BUIDL's Assets Entered DeFi Without Anyone Pushing. What This Tells GS DAP.")

if __name__ == '__main__':
    main()
