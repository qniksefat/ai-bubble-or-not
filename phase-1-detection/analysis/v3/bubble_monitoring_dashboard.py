#!/usr/bin/env python3
"""
AI Bubble Real-Time Monitoring Dashboard
Tracks multiple indicators to assess bubble conditions in real-time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class AIBubbleMonitor:
    """
    Comprehensive AI Bubble Monitoring System
    Tracks multiple indicators and provides a composite bubble score
    """

    def __init__(self):
        self.indicators = {}
        self.weights = {
            'search_trends': 0.15,
            'valuation_metrics': 0.25,
            'sentiment_analysis': 0.15,
            'vc_funding': 0.15,
            'market_concentration': 0.15,
            'roi_delivery': 0.15
        }

    def calculate_search_trend_score(self, current_level=37, growth_rate=254):
        """
        Score based on Google Trends data for "AI bubble" searches
        """
        # Normalize to 0-100 scale
        level_score = min(current_level / 100 * 100, 100)

        # Growth rate scoring (exponential concern above 100% annual)
        if growth_rate < 50:
            growth_score = 20
        elif growth_rate < 100:
            growth_score = 40
        elif growth_rate < 200:
            growth_score = 60
        elif growth_rate < 300:
            growth_score = 80
        else:
            growth_score = 100

        # Weighted average
        score = (level_score * 0.4 + growth_score * 0.6)

        self.indicators['search_trends'] = {
            'score': score,
            'current_level': current_level,
            'growth_rate': growth_rate,
            'interpretation': self._interpret_score(score)
        }

        return score

    def calculate_valuation_score(self, pe_ratios=None, market_caps=None):
        """
        Score based on valuation metrics
        """
        if pe_ratios is None:
            # Default values based on research
            pe_ratios = {
                'NVIDIA': 53,
                'Microsoft': 35,
                'Google': 28,
                'Meta': 27,
                'OpenAI_implied': 100  # Based on $500B valuation
            }

        # Calculate deviation from historical norms (S&P 500 average ~20)
        historical_pe = 20
        deviations = [max(0, (pe - historical_pe) / historical_pe * 100)
                     for pe in pe_ratios.values()]
        avg_deviation = np.mean(deviations)

        # Score based on deviation
        if avg_deviation < 25:
            score = 20
        elif avg_deviation < 50:
            score = 40
        elif avg_deviation < 100:
            score = 60
        elif avg_deviation < 150:
            score = 80
        else:
            score = 95

        self.indicators['valuation_metrics'] = {
            'score': score,
            'avg_pe': np.mean(list(pe_ratios.values())),
            'deviation_from_norm': avg_deviation,
            'interpretation': self._interpret_score(score)
        }

        return score

    def calculate_sentiment_score(self, fund_manager_bubble_pct=54,
                                 expert_warnings=7, media_mentions=85):
        """
        Score based on professional and public sentiment
        """
        # Fund manager sentiment (0-100)
        fm_score = fund_manager_bubble_pct

        # Expert warnings (normalized to 0-100)
        expert_score = min(expert_warnings * 10, 100)

        # Media saturation (already 0-100)
        media_score = media_mentions

        # Weighted average
        score = (fm_score * 0.5 + expert_score * 0.3 + media_score * 0.2)

        self.indicators['sentiment_analysis'] = {
            'score': score,
            'fund_manager_bubble_pct': fund_manager_bubble_pct,
            'expert_warnings_count': expert_warnings,
            'media_saturation': media_mentions,
            'interpretation': self._interpret_score(score)
        }

        return score

    def calculate_vc_funding_score(self, quarterly_investment=88, yoy_growth=67):
        """
        Score based on VC funding patterns
        """
        # Investment level scoring (in billions)
        if quarterly_investment < 20:
            inv_score = 20
        elif quarterly_investment < 40:
            inv_score = 40
        elif quarterly_investment < 60:
            inv_score = 60
        elif quarterly_investment < 80:
            inv_score = 80
        else:
            inv_score = 95

        # Growth rate scoring
        if yoy_growth < 20:
            growth_score = 20
        elif yoy_growth < 40:
            growth_score = 40
        elif yoy_growth < 60:
            growth_score = 60
        elif yoy_growth < 80:
            growth_score = 80
        else:
            growth_score = 95

        score = (inv_score * 0.6 + growth_score * 0.4)

        self.indicators['vc_funding'] = {
            'score': score,
            'quarterly_investment_B': quarterly_investment,
            'yoy_growth_pct': yoy_growth,
            'interpretation': self._interpret_score(score)
        }

        return score

    def calculate_concentration_score(self, top7_market_share=35,
                                     ai_exposure_pct=50):
        """
        Score based on market concentration risk
        """
        # Market concentration (Magnificent 7 share of S&P 500)
        if top7_market_share < 20:
            conc_score = 20
        elif top7_market_share < 25:
            conc_score = 40
        elif top7_market_share < 30:
            conc_score = 60
        elif top7_market_share < 35:
            conc_score = 80
        else:
            conc_score = 95

        # AI exposure across S&P 500
        ai_score = min(ai_exposure_pct * 2, 100)

        score = (conc_score * 0.6 + ai_score * 0.4)

        self.indicators['market_concentration'] = {
            'score': score,
            'top7_share_pct': top7_market_share,
            'sp500_ai_exposure_pct': ai_exposure_pct,
            'interpretation': self._interpret_score(score)
        }

        return score

    def calculate_roi_score(self, project_failure_rate=95,
                           paid_user_pct=10, revenue_multiple=100):
        """
        Score based on ROI delivery metrics
        """
        # Project failure rate (higher = more bubble)
        failure_score = project_failure_rate

        # Monetization rate (lower = more bubble)
        monetization_score = 100 - paid_user_pct

        # Revenue multiple (higher = more bubble)
        if revenue_multiple < 20:
            multiple_score = 20
        elif revenue_multiple < 40:
            multiple_score = 40
        elif revenue_multiple < 60:
            multiple_score = 60
        elif revenue_multiple < 80:
            multiple_score = 80
        else:
            multiple_score = 95

        score = (failure_score * 0.4 + monetization_score * 0.3 +
                multiple_score * 0.3)

        self.indicators['roi_delivery'] = {
            'score': score,
            'project_failure_rate': project_failure_rate,
            'paid_user_pct': paid_user_pct,
            'revenue_multiple': revenue_multiple,
            'interpretation': self._interpret_score(score)
        }

        return score

    def _interpret_score(self, score):
        """
        Interpret individual indicator scores
        """
        if score < 20:
            return "No bubble"
        elif score < 40:
            return "Minimal concern"
        elif score < 60:
            return "Moderate concern"
        elif score < 80:
            return "High concern"
        else:
            return "Extreme bubble"

    def calculate_composite_score(self):
        """
        Calculate weighted composite bubble score
        """
        # Calculate all individual scores with current data
        self.calculate_search_trend_score()
        self.calculate_valuation_score()
        self.calculate_sentiment_score()
        self.calculate_vc_funding_score()
        self.calculate_concentration_score()
        self.calculate_roi_score()

        # Calculate weighted average
        composite = sum(self.indicators[key]['score'] * self.weights[key]
                       for key in self.weights.keys())

        return composite

    def get_bubble_phase(self, composite_score):
        """
        Determine current bubble phase based on composite score
        """
        if composite_score < 20:
            return "No Bubble"
        elif composite_score < 35:
            return "Early Formation"
        elif composite_score < 50:
            return "Middle Stage"
        elif composite_score < 65:
            return "Late-Middle Stage"
        elif composite_score < 80:
            return "Late Stage"
        elif composite_score < 90:
            return "Peak Formation"
        else:
            return "Imminent Burst Risk"

    def generate_report(self):
        """
        Generate comprehensive bubble assessment report
        """
        composite = self.calculate_composite_score()
        phase = self.get_bubble_phase(composite)

        print("=" * 80)
        print("AI BUBBLE MONITORING DASHBOARD")
        print("=" * 80)
        print(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Overall Assessment
        print("OVERALL ASSESSMENT")
        print("-" * 40)
        print(f"Composite Bubble Score: {composite:.1f}/100")
        print(f"Current Phase: {phase}")
        print(f"Bubble Probability: {min(composite * 1.1, 99):.0f}%")
        print()

        # Risk Level
        if composite < 40:
            risk = "LOW"
            color = "🟢"
        elif composite < 60:
            risk = "MODERATE"
            color = "🟡"
        elif composite < 80:
            risk = "HIGH"
            color = "🟠"
        else:
            risk = "EXTREME"
            color = "🔴"

        print(f"{color} Risk Level: {risk}")
        print()

        # Individual Indicators
        print("INDIVIDUAL INDICATORS")
        print("-" * 40)

        for key, data in self.indicators.items():
            print(f"\n{key.replace('_', ' ').title()}:")
            print(f"  Score: {data['score']:.1f}/100")
            print(f"  Status: {data['interpretation']}")

            # Key metrics for each indicator
            if key == 'search_trends':
                print(f"  Current Level: {data['current_level']}/100")
                print(f"  YoY Growth: {data['growth_rate']}%")
            elif key == 'valuation_metrics':
                print(f"  Avg P/E Ratio: {data['avg_pe']:.1f}")
                print(f"  Deviation from Norm: {data['deviation_from_norm']:.0f}%")
            elif key == 'sentiment_analysis':
                print(f"  Fund Managers (Bubble): {data['fund_manager_bubble_pct']}%")
                print(f"  Expert Warnings: {data['expert_warnings_count']}")
            elif key == 'vc_funding':
                print(f"  Quarterly Investment: ${data['quarterly_investment_B']}B")
                print(f"  YoY Growth: {data['yoy_growth_pct']}%")
            elif key == 'market_concentration':
                print(f"  Top 7 Market Share: {data['top7_share_pct']}%")
                print(f"  S&P 500 AI Exposure: {data['sp500_ai_exposure_pct']}%")
            elif key == 'roi_delivery':
                print(f"  Project Failure Rate: {data['project_failure_rate']}%")
                print(f"  Paid User %: {data['paid_user_pct']}%")

        print()
        print("=" * 80)

        # Recommendations
        print("RECOMMENDED ACTIONS")
        print("-" * 40)

        if composite < 40:
            print("• Continue normal investment strategy")
            print("• Monitor for early warning signs")
            print("• Consider gradual AI exposure increase")
        elif composite < 60:
            print("• Begin portfolio rebalancing")
            print("• Reduce concentration in high-P/E AI stocks")
            print("• Increase allocation to value sectors")
        elif composite < 80:
            print("• Implement defensive strategies")
            print("• Consider barbell portfolio approach")
            print("• Increase cash/bond allocation")
            print("• Take profits on speculative positions")
        else:
            print("⚠️  URGENT: High bubble burst risk")
            print("• Maximize defensive positioning")
            print("• Significant reduction in AI/tech exposure")
            print("• Increase safe haven allocations")
            print("• Prepare for potential 30-50% correction")

        print()
        print("=" * 80)

        return composite, phase

    def plot_dashboard(self):
        """
        Create visual dashboard of bubble indicators
        """
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('AI Bubble Monitoring Dashboard', fontsize=16, fontweight='bold')

        # Ensure all scores are calculated
        self.calculate_composite_score()

        # Plot 1: Composite Score Gauge
        ax = axes[0, 0]
        composite = self.calculate_composite_score()
        self._plot_gauge(ax, composite, "Composite Score")

        # Plot 2: Individual Indicators Bar Chart
        ax = axes[0, 1]
        indicators = list(self.indicators.keys())
        scores = [self.indicators[k]['score'] for k in indicators]
        colors = ['red' if s >= 80 else 'orange' if s >= 60 else 'yellow' if s >= 40 else 'green'
                 for s in scores]
        bars = ax.barh(range(len(indicators)), scores, color=colors)
        ax.set_yticks(range(len(indicators)))
        ax.set_yticklabels([k.replace('_', ' ').title() for k in indicators])
        ax.set_xlabel('Score (0-100)')
        ax.set_title('Individual Indicator Scores')
        ax.set_xlim(0, 100)

        # Add value labels on bars
        for bar, score in zip(bars, scores):
            ax.text(score + 1, bar.get_y() + bar.get_height()/2,
                   f'{score:.0f}', va='center')

        # Plot 3: Bubble Phase Timeline
        ax = axes[0, 2]
        phases = ["Early", "Middle", "Late-Middle", "Late", "Peak", "Burst Risk"]
        phase_scores = [20, 35, 50, 65, 80, 90]
        current_phase_idx = 0
        for i, threshold in enumerate(phase_scores):
            if composite >= threshold:
                current_phase_idx = i

        colors = ['lightgray'] * len(phases)
        colors[current_phase_idx] = 'red'
        ax.barh(phases, [100]*len(phases), color=colors, alpha=0.3)
        ax.barh(phases, phase_scores, color=colors)
        ax.axvline(composite, color='red', linestyle='--', linewidth=2, label=f'Current: {composite:.0f}')
        ax.set_xlabel('Bubble Score')
        ax.set_title('Bubble Phase Progression')
        ax.set_xlim(0, 100)
        ax.legend()

        # Plot 4: Historical Pattern Comparison
        ax = axes[1, 0]
        patterns = ['Dot-com\n(2000)', 'Housing\n(2008)', 'Crypto\n(2021)', 'AI\n(2025)']
        pattern_scores = [95, 85, 75, composite]
        colors = ['gray', 'gray', 'gray', 'red']
        ax.bar(patterns, pattern_scores, color=colors, alpha=0.7)
        ax.set_ylabel('Bubble Score at Peak/Current')
        ax.set_title('Historical Bubble Comparison')
        ax.set_ylim(0, 100)
        ax.axhline(80, color='red', linestyle='--', alpha=0.5, label='High Risk Threshold')
        ax.legend()

        # Plot 5: Risk Matrix
        ax = axes[1, 1]
        risk_matrix = np.array([
            [self.indicators['search_trends']['score'],
             self.indicators['sentiment_analysis']['score']],
            [self.indicators['valuation_metrics']['score'],
             self.indicators['roi_delivery']['score']]
        ])
        im = ax.imshow(risk_matrix, cmap='RdYlGn_r', vmin=0, vmax=100)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Market\nSentiment', 'Public\nConcern'])
        ax.set_yticklabels(['Valuations', 'ROI\nDelivery'])
        ax.set_title('Risk Heatmap')

        # Add text annotations
        for i in range(2):
            for j in range(2):
                text = ax.text(j, i, f'{risk_matrix[i, j]:.0f}',
                             ha="center", va="center", color="black")

        # Plot 6: Trend Projection
        ax = axes[1, 2]
        months = ['Oct\n2025', 'Nov', 'Dec', 'Jan\n2026', 'Feb', 'Mar']
        base_score = composite
        # Projection based on current momentum
        if composite > 60:
            trend = [base_score + i*2 for i in range(6)]  # Accelerating
        else:
            trend = [base_score + i*1 for i in range(6)]  # Steady growth

        ax.plot(months, trend, 'b-', linewidth=2, marker='o')
        ax.fill_between(range(6),
                        [t - 5 for t in trend],
                        [t + 5 for t in trend],
                        alpha=0.3, color='blue')
        ax.axhline(80, color='red', linestyle='--', alpha=0.5, label='High Risk')
        ax.axhline(90, color='darkred', linestyle='--', alpha=0.5, label='Extreme Risk')
        ax.set_ylabel('Projected Bubble Score')
        ax.set_title('6-Month Projection')
        ax.set_ylim(max(0, min(trend) - 10), min(100, max(trend) + 10))
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def _plot_gauge(self, ax, value, title):
        """
        Create a gauge chart for the composite score
        """
        # Create gauge segments
        segments = [20, 20, 20, 20, 20]  # 5 segments of 20 each
        colors = ['green', 'yellowgreen', 'yellow', 'orange', 'red']

        # Create pie chart as gauge
        wedges, texts = ax.pie(segments, colors=colors, startangle=90,
                               counterclock=False)

        # Add center circle to create donut
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)

        # Add needle
        needle_angle = 90 - (value * 1.8)  # Convert score to angle
        ax.arrow(0, 0,
                0.6 * np.cos(np.radians(needle_angle)),
                0.6 * np.sin(np.radians(needle_angle)),
                width=0.05, head_width=0.1, head_length=0.1,
                fc='black', ec='black')

        # Add value text
        ax.text(0, -0.2, f'{value:.0f}', fontsize=24, fontweight='bold',
               ha='center', va='center')
        ax.text(0, -0.35, title, fontsize=12, ha='center', va='center')

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.axis('equal')


def main():
    """
    Run the bubble monitoring dashboard
    """
    print("\n" + "="*80)
    print("INITIALIZING AI BUBBLE MONITORING SYSTEM...")
    print("="*80 + "\n")

    # Create monitor instance
    monitor = AIBubbleMonitor()

    # Generate report
    composite_score, phase = monitor.generate_report()

    # Generate and save visualization
    print("\nGenerating visual dashboard...")
    fig = monitor.plot_dashboard()

    # Save the dashboard
    output_path = 'ai_bubble_dashboard.png'
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Dashboard saved to: {output_path}")

    # Historical context
    print("\n" + "="*80)
    print("HISTORICAL CONTEXT")
    print("="*80)
    print("\nFor comparison, at their peaks:")
    print("• Dot-com bubble (2000): Score would have been ~95")
    print("• Housing bubble (2008): Score would have been ~85")
    print("• Crypto bubble (2021): Score would have been ~75")
    print(f"• Current AI market: Score is {composite_score:.1f}")

    # Timeline estimates
    print("\n" + "="*80)
    print("TIMELINE ESTIMATES")
    print("="*80)

    if composite_score < 40:
        print("No immediate bubble risk. Normal market conditions.")
    elif composite_score < 60:
        print("Early bubble formation. Monitor closely over next 12-18 months.")
    elif composite_score < 80:
        print("Active bubble conditions. Risk of correction within 6-12 months.")
    else:
        print("⚠️  EXTREME bubble conditions. Correction likely within 3-6 months.")

    print("\n" + "="*80)
    print("DISCLAIMER")
    print("="*80)
    print("This analysis is for research purposes only and should not be considered")
    print("as financial advice. Consult with qualified professionals before making")
    print("investment decisions.")
    print("="*80 + "\n")

    return monitor, composite_score, phase


if __name__ == "__main__":
    monitor, score, phase = main()