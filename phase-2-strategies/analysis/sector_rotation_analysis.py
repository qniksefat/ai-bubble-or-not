#!/usr/bin/env python3
"""
Sector Rotation Analysis During Tech Bubble Corrections
Analyzes which sectors historically benefit when tech corrects
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

plt.style.use('seaborn-v0_8-darkgrid')

class SectorRotationAnalyzer:
    """
    Analyzes sector performance patterns during tech corrections
    """

    def __init__(self):
        # Historical data from major tech corrections
        self.corrections = {
            'Dot-com Crash (2000-2002)': {
                'tech_performance': -78,  # NASDAQ fell 78%
                'sector_performance': {
                    'Technology': -78,
                    'Consumer Discretionary': -45,
                    'Financials': -35,
                    'Healthcare': -20,
                    'Industrials': -30,
                    'Energy': +15,
                    'Utilities': +10,
                    'Consumer Staples': +5,
                    'Real Estate': +8,
                    'Materials': -10,
                    'Gold/Precious Metals': +25
                }
            },
            'Financial Crisis (2008-2009)': {
                'tech_performance': -55,
                'sector_performance': {
                    'Technology': -55,
                    'Financials': -83,
                    'Consumer Discretionary': -54,
                    'Industrials': -57,
                    'Energy': -56,
                    'Materials': -60,
                    'Healthcare': -39,
                    'Consumer Staples': -29,
                    'Utilities': -38,
                    'Real Estate': -68,
                    'Gold/Precious Metals': +25
                }
            },
            'COVID Crash (2020)': {
                'tech_performance': -30,
                'sector_performance': {
                    'Technology': -30,
                    'Energy': -65,
                    'Financials': -40,
                    'Industrials': -38,
                    'Real Estate': -35,
                    'Materials': -33,
                    'Utilities': -30,
                    'Consumer Discretionary': -28,
                    'Healthcare': -23,
                    'Consumer Staples': -20,
                    'Gold/Precious Metals': +5
                }
            },
            'Tech Correction (2022)': {
                'tech_performance': -35,
                'sector_performance': {
                    'Technology': -35,
                    'Consumer Discretionary': -37,
                    'Real Estate': -28,
                    'Financials': -12,
                    'Materials': -14,
                    'Industrials': -7,
                    'Healthcare': -5,
                    'Consumer Staples': -3,
                    'Utilities': +2,
                    'Energy': +48,
                    'Gold/Precious Metals': -5
                }
            }
        }

        # Current AI bubble specifics
        self.ai_bubble_sectors = {
            'High Risk (Direct AI Exposure)': [
                'NVIDIA', 'AMD', 'Microsoft', 'Google', 'Meta',
                'OpenAI', 'Anthropic', 'Palantir', 'C3.ai'
            ],
            'Medium Risk (AI Adjacent)': [
                'Apple', 'Amazon', 'Tesla', 'Adobe', 'Salesforce',
                'ServiceNow', 'Snowflake', 'MongoDB'
            ],
            'Low Risk (Traditional Tech)': [
                'Oracle', 'IBM', 'Cisco', 'Intel', 'HP'
            ],
            'Potential Beneficiaries': [
                'Energy', 'Utilities', 'Consumer Staples', 'Healthcare',
                'Value Stocks', 'International Markets', 'Gold'
            ]
        }

    def analyze_historical_patterns(self):
        """
        Analyze historical sector rotation patterns
        """
        print("=" * 80)
        print("HISTORICAL SECTOR ROTATION PATTERNS DURING TECH CORRECTIONS")
        print("=" * 80)

        # Calculate average performance across corrections
        all_sectors = set()
        for correction in self.corrections.values():
            all_sectors.update(correction['sector_performance'].keys())

        avg_performance = {}
        for sector in all_sectors:
            performances = []
            for correction in self.corrections.values():
                if sector in correction['sector_performance']:
                    performances.append(correction['sector_performance'][sector])
            avg_performance[sector] = np.mean(performances) if performances else 0

        # Sort by average performance
        sorted_sectors = sorted(avg_performance.items(),
                              key=lambda x: x[1], reverse=True)

        print("\nAverage Sector Performance During Tech Corrections:")
        print("-" * 50)
        for sector, perf in sorted_sectors:
            if perf > 0:
                indicator = "📈"
                color = "OUTPERFORMER"
            elif perf > -20:
                indicator = "➡️"
                color = "DEFENSIVE"
            else:
                indicator = "📉"
                color = "UNDERPERFORMER"

            print(f"{indicator} {sector:25s}: {perf:+6.1f}%  [{color}]")

        return avg_performance

    def project_ai_bubble_correction(self, correction_magnitude=40):
        """
        Project potential sector performance in AI bubble correction
        """
        print("\n" + "=" * 80)
        print("PROJECTED SECTOR PERFORMANCE IN AI BUBBLE CORRECTION")
        print("=" * 80)
        print(f"Assumption: {correction_magnitude}% tech sector correction")
        print("-" * 50)

        # Based on historical patterns, project performance
        projections = {
            'AI/Tech Leaders': -correction_magnitude * 1.2,  # Overcorrection
            'Broader Technology': -correction_magnitude,
            'Consumer Discretionary': -correction_magnitude * 0.8,
            'Financials': -correction_magnitude * 0.6,
            'Industrials': -correction_magnitude * 0.5,
            'Healthcare': -correction_magnitude * 0.3,
            'Consumer Staples': -correction_magnitude * 0.2,
            'Utilities': correction_magnitude * 0.1,  # Slight positive
            'Energy': correction_magnitude * 0.2,  # Beneficiary
            'Gold/Precious Metals': correction_magnitude * 0.3,  # Safe haven
            'Value Stocks': -correction_magnitude * 0.25,
            'International (Non-US)': -correction_magnitude * 0.4,
            'Bonds/Treasuries': correction_magnitude * 0.15
        }

        sorted_projections = sorted(projections.items(),
                                  key=lambda x: x[1], reverse=True)

        print("\nProjected Performance by Sector/Asset Class:")
        for sector, perf in sorted_projections:
            bars = '█' * int(abs(perf) / 5)
            if perf > 0:
                print(f"📈 {sector:25s}: {perf:+6.1f}% {bars}")
            else:
                print(f"📉 {sector:25s}: {perf:+6.1f}% {bars}")

        return projections

    def recommend_rotation_strategy(self):
        """
        Recommend specific rotation strategies
        """
        print("\n" + "=" * 80)
        print("RECOMMENDED SECTOR ROTATION STRATEGIES")
        print("=" * 80)

        strategies = {
            'Immediate Actions (Now)': [
                'Reduce exposure to high P/E AI stocks (NVIDIA, AI startups)',
                'Take profits on stocks up >100% in past year',
                'Rotate into defensive sectors (Staples, Utilities, Healthcare)',
                'Increase allocation to value stocks (P/E < 20)',
                'Add international diversification (Europe, Asia)',
                'Consider gold/precious metals allocation (5-10%)'
            ],
            '3-Month Strategy': [
                'Monitor tech earnings for disappointments',
                'Build cash position for opportunities (20-30%)',
                'Research quality tech names for post-correction buying',
                'Increase bond allocation if yields rise',
                'Focus on companies with real AI revenue (not promises)'
            ],
            '6-Month Strategy': [
                'Prepare shopping list of quality AI stocks',
                'Look for 30-50% discounts from peaks',
                'Begin selective re-entry into tech leaders',
                'Maintain defensive tilt until stabilization',
                'Watch for capitulation indicators'
            ],
            'Post-Correction (12+ months)': [
                'Aggressive re-entry into quality tech',
                'Focus on AI infrastructure plays',
                'Identify next-generation AI winners',
                'Reduce defensive positions',
                'Return to growth-oriented allocation'
            ]
        }

        for timeframe, actions in strategies.items():
            print(f"\n{timeframe}:")
            for i, action in enumerate(actions, 1):
                print(f"  {i}. {action}")

        return strategies

    def identify_specific_opportunities(self):
        """
        Identify specific investment opportunities
        """
        print("\n" + "=" * 80)
        print("SPECIFIC OPPORTUNITIES BY CATEGORY")
        print("=" * 80)

        opportunities = {
            'Safe Haven Assets': {
                'Gold ETFs': ['GLD', 'IAU', 'SGOL'],
                'Treasury Bonds': ['TLT', 'IEF', 'SHY'],
                'Cash Equivalents': ['Money Market Funds', 'T-Bills'],
                'Rating': '🛡️ DEFENSIVE'
            },
            'Defensive Sectors': {
                'Consumer Staples': ['XLP', 'VDC', 'PG', 'KO', 'PEP'],
                'Utilities': ['XLU', 'VPU', 'NEE', 'DUK'],
                'Healthcare': ['XLV', 'VHT', 'JNJ', 'UNH', 'PFE'],
                'Rating': '🏥 RESILIENT'
            },
            'Value Opportunities': {
                'Financial Value': ['JPM', 'BAC', 'WFC', 'BRK.B'],
                'Energy': ['XLE', 'VDE', 'XOM', 'CVX'],
                'International Value': ['VEA', 'EFA', 'VWO'],
                'Rating': '💎 VALUE PLAYS'
            },
            'Contrarian Plays': {
                'Beaten-down Quality Tech': ['INTC', 'IBM', 'CSCO'],
                'Non-AI Growth': ['Healthcare innovation', 'Clean energy'],
                'Small-cap Value': ['IWM', 'VB'],
                'Rating': '🎯 CONTRARIAN'
            },
            'Post-Correction Shopping List': {
                'Quality AI Infrastructure': ['MSFT', 'GOOGL', 'AMZN'],
                'Semiconductor Leaders': ['NVDA (after 40%+ drop)', 'AMD'],
                'AI Software': ['SNOW', 'MDB', 'PLTR'],
                'Rating': '🚀 FUTURE LEADERS'
            }
        }

        for category, details in opportunities.items():
            print(f"\n{category} {details['Rating']}:")
            for subcategory, items in details.items():
                if subcategory != 'Rating':
                    print(f"  • {subcategory}: {', '.join(items)}")

        return opportunities

    def calculate_risk_adjusted_allocation(self, risk_tolerance='moderate'):
        """
        Calculate recommended portfolio allocation based on risk tolerance
        """
        print("\n" + "=" * 80)
        print("RISK-ADJUSTED PORTFOLIO ALLOCATIONS")
        print("=" * 80)

        allocations = {
            'conservative': {
                'Cash/T-Bills': 30,
                'Bonds/Treasuries': 30,
                'Defensive Sectors': 20,
                'International': 10,
                'Gold': 10,
                'Tech/Growth': 0
            },
            'moderate': {
                'Cash/T-Bills': 20,
                'Bonds/Treasuries': 20,
                'Defensive Sectors': 25,
                'Value Stocks': 15,
                'International': 10,
                'Gold': 5,
                'Tech/Growth': 5
            },
            'aggressive': {
                'Cash/T-Bills': 10,
                'Bonds/Treasuries': 10,
                'Defensive Sectors': 15,
                'Value Stocks': 20,
                'International': 15,
                'Beaten-down Tech': 20,
                'Gold': 5,
                'High-Risk AI': 5
            }
        }

        allocation = allocations.get(risk_tolerance, allocations['moderate'])

        print(f"\nRecommended Allocation for {risk_tolerance.upper()} investors:")
        print("-" * 50)

        total = 0
        for asset, pct in sorted(allocation.items(),
                                key=lambda x: x[1], reverse=True):
            bars = '█' * int(pct / 5)
            print(f"{asset:25s}: {pct:3d}% {bars}")
            total += pct

        print(f"{'Total':25s}: {total:3d}%")

        return allocation

    def generate_visual_analysis(self):
        """
        Generate visual analysis of sector rotation
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Sector Rotation Analysis - AI Bubble Correction',
                    fontsize=16, fontweight='bold')

        # Plot 1: Historical Correction Patterns
        ax = axes[0, 0]
        corrections = list(self.corrections.keys())
        tech_perfs = [self.corrections[c]['tech_performance'] for c in corrections]
        colors = ['red' if p < -50 else 'orange' if p < -30 else 'yellow'
                 for p in tech_perfs]

        bars = ax.bar(range(len(corrections)), tech_perfs, color=colors)
        ax.set_xticks(range(len(corrections)))
        ax.set_xticklabels([c.split('(')[0].strip() for c in corrections],
                          rotation=45, ha='right')
        ax.set_ylabel('Tech Sector Performance (%)')
        ax.set_title('Historical Tech Corrections')
        ax.axhline(0, color='black', linestyle='-', linewidth=0.5)

        # Add value labels
        for bar, val in zip(bars, tech_perfs):
            ax.text(bar.get_x() + bar.get_width()/2, val - 3,
                   f'{val}%', ha='center', va='top')

        # Plot 2: Sector Performance Heatmap
        ax = axes[0, 1]
        # Create matrix of sector performances across corrections
        sectors = ['Tech', 'Financials', 'Healthcare', 'Staples',
                  'Energy', 'Utilities', 'Gold']
        matrix = []
        for correction in self.corrections.values():
            row = []
            for sector in sectors:
                sector_map = {
                    'Tech': 'Technology',
                    'Financials': 'Financials',
                    'Healthcare': 'Healthcare',
                    'Staples': 'Consumer Staples',
                    'Energy': 'Energy',
                    'Utilities': 'Utilities',
                    'Gold': 'Gold/Precious Metals'
                }
                mapped = sector_map.get(sector, sector)
                value = correction['sector_performance'].get(mapped, 0)
                row.append(value)
            matrix.append(row)

        im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=-80, vmax=50)
        ax.set_xticks(range(len(sectors)))
        ax.set_xticklabels(sectors, rotation=45, ha='right')
        ax.set_yticks(range(len(corrections)))
        ax.set_yticklabels([c.split('(')[0].strip() for c in corrections])
        ax.set_title('Sector Performance Across Corrections')

        # Add colorbar
        plt.colorbar(im, ax=ax, label='Performance (%)')

        # Plot 3: Projected AI Bubble Correction
        ax = axes[1, 0]
        projections = self.project_ai_bubble_correction(40)
        sorted_proj = sorted(projections.items(), key=lambda x: x[1])
        sectors = [s for s, _ in sorted_proj]
        values = [v for _, v in sorted_proj]
        colors = ['green' if v > 0 else 'red' for v in values]

        bars = ax.barh(range(len(sectors)), values, color=colors, alpha=0.7)
        ax.set_yticks(range(len(sectors)))
        ax.set_yticklabels(sectors)
        ax.set_xlabel('Projected Performance (%)')
        ax.set_title('Projected Performance in AI Bubble Correction (-40%)')
        ax.axvline(0, color='black', linestyle='-', linewidth=1)

        # Plot 4: Risk-Adjusted Allocation Pie Chart
        ax = axes[1, 1]
        allocation = self.calculate_risk_adjusted_allocation('moderate')
        sizes = list(allocation.values())
        labels = list(allocation.keys())
        colors = plt.cm.Set3(range(len(labels)))

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct='%1.0f%%', startangle=90)
        ax.set_title('Recommended Portfolio Allocation (Moderate Risk)')

        plt.tight_layout()
        return fig


def main():
    """
    Run sector rotation analysis
    """
    analyzer = SectorRotationAnalyzer()

    # Run analyses
    avg_performance = analyzer.analyze_historical_patterns()
    projections = analyzer.project_ai_bubble_correction()
    strategies = analyzer.recommend_rotation_strategy()
    opportunities = analyzer.identify_specific_opportunities()

    # Generate allocations for different risk profiles
    print("\n" + "=" * 80)
    print("PORTFOLIO ALLOCATIONS BY RISK PROFILE")
    print("=" * 80)

    for risk_level in ['conservative', 'moderate', 'aggressive']:
        analyzer.calculate_risk_adjusted_allocation(risk_level)
        print()

    # Generate and save visualization
    print("Generating visual analysis...")
    fig = analyzer.generate_visual_analysis()
    output_path = 'sector_rotation_analysis.png'
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Analysis saved to: {output_path}")

    # Key takeaways
    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
1. DEFENSIVE POSITIONING IS CRITICAL
   - History shows tech corrections spread to other sectors
   - Consumer staples, utilities, and healthcare typically outperform

2. CASH IS A POSITION
   - Having 20-30% cash provides optionality
   - Allows aggressive buying during capitulation

3. GEOGRAPHIC DIVERSIFICATION HELPS
   - International markets often correct less
   - Currency effects can provide cushion

4. QUALITY MATTERS IN CORRECTIONS
   - Companies with real revenue hold up better
   - Speculative names get hit hardest

5. TIMING IS DIFFICULT
   - Begin rotation early rather than late
   - Don't try to catch falling knives
    """)

    print("=" * 80)
    print("Disclaimer: For research purposes only. Not financial advice.")
    print("=" * 80)

    return analyzer


if __name__ == "__main__":
    analyzer = main()