import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('multiTimeline-googleTrends.csv', skiprows=1)
df['Week'] = pd.to_datetime(df['Week'])
df.set_index('Week', inplace=True)

# Rename columns for easier access
df.columns = ['ai_bubble', 'ai_startup', 'prompt_engineering', 'ai_roadmap', 'langchain']

# Convert to numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# CRITICAL INSIGHT: Filter for post-ChatGPT era (2023 onwards)
# This is when AI bubble concerns became meaningful
df_relevant = df['2023-01-01':]

print("="*80)
print("AI BUBBLE ANALYSIS - REFINED POST-CHATGPT ERA FOCUS")
print("="*80)
print(f"\nAnalysis Period: {df_relevant.index[0].date()} to {df_relevant.index[-1].date()}")
print(f"Weeks analyzed: {len(df_relevant)}")

# Add monthly and quarterly aggregations for better insights
df_monthly = df_relevant.resample('M').mean()
df_quarterly = df_relevant.resample('Q').mean()

# Key periods identification
chatgpt_launch = df['2022-12-01':'2023-01-31']  # ChatGPT launch period
gpt4_launch = df['2023-03-01':'2023-04-30']  # GPT-4 launch period
recent_surge = df['2025-05-01':]  # Recent dramatic surge

print("\n" + "="*80)
print("1. CRITICAL PERIODS ANALYSIS")
print("="*80)

print("\nKey AI Development Milestones & Bubble Response:")
print(f"\n📅 ChatGPT Launch Period (Dec 2022 - Jan 2023):")
print(f"  - AI Bubble searches: {chatgpt_launch['ai_bubble'].mean():.1f}")
print(f"  - Prompt Engineering: {chatgpt_launch['prompt_engineering'].mean():.1f}")

print(f"\n📅 GPT-4 Launch Period (Mar-Apr 2023):")
print(f"  - AI Bubble searches: {gpt4_launch['ai_bubble'].mean():.1f}")
print(f"  - Prompt Engineering: {gpt4_launch['prompt_engineering'].mean():.1f}")

print(f"\n📅 Recent Surge (May 2025 - Present):")
print(f"  - AI Bubble searches: {recent_surge['ai_bubble'].mean():.1f}")
print(f"  - AI Startup searches: {recent_surge['ai_startup'].mean():.1f}")

# Phase Analysis with monthly aggregation
print("\n" + "="*80)
print("2. BUBBLE EVOLUTION PHASES (Monthly Averages)")
print("="*80)

# Define clear phases based on monthly averages
phases = []
for date, row in df_monthly.iterrows():
    ai_bubble_val = row['ai_bubble']
    if ai_bubble_val < 2:
        phase = "Pre-awareness"
    elif ai_bubble_val < 5:
        phase = "Early Concern"
    elif ai_bubble_val < 10:
        phase = "Growing Anxiety"
    elif ai_bubble_val < 20:
        phase = "High Alert"
    else:
        phase = "Peak Fear"
    phases.append((date.strftime('%Y-%m'), ai_bubble_val, phase))

print("\nMonthly Phase Progression (Last 12 months):")
for month, value, phase in phases[-12:]:
    bar = '█' * int(value/2)
    print(f"  {month}: {bar:<20} {value:5.1f} - {phase}")

# Year-over-Year comparison
print("\n" + "="*80)
print("3. YEAR-OVER-YEAR COMPARISON")
print("="*80)

for year in [2023, 2024, 2025]:
    year_start = f'{year}-01-01'
    year_end = f'{year}-12-31'
    year_data = df[year_start:year_end]
    if len(year_data) > 0:
        print(f"\n{year} Statistics:")
        print(f"  - AI Bubble avg: {year_data['ai_bubble'].mean():.2f}")
        print(f"  - AI Bubble max: {year_data['ai_bubble'].max():.0f}")
        print(f"  - Prompt Engineering avg: {year_data['prompt_engineering'].mean():.1f}")
        print(f"  - AI Startup avg: {year_data['ai_startup'].mean():.1f}")

# Acceleration Analysis
print("\n" + "="*80)
print("4. ACCELERATION ANALYSIS (Post-2023)")
print("="*80)

# Calculate quarter-over-quarter growth
qoq_growth = []
for i in range(1, len(df_quarterly)):
    if df_quarterly['ai_bubble'].iloc[i-1] > 0:
        growth = ((df_quarterly['ai_bubble'].iloc[i] / df_quarterly['ai_bubble'].iloc[i-1]) - 1) * 100
        quarter_name = df_quarterly.index[i].strftime('%Y Q%q')
        qoq_growth.append((quarter_name, growth))

print("\nQuarter-over-Quarter Growth in AI Bubble Searches:")
for quarter, growth in qoq_growth[-6:]:  # Last 6 quarters
    direction = "↑" if growth > 0 else "↓"
    print(f"  {quarter}: {direction} {abs(growth):.1f}%")

# Rolling averages for trend smoothing
df_relevant['ai_bubble_ma4'] = df_relevant['ai_bubble'].rolling(window=4).mean()  # 1-month MA
df_relevant['ai_bubble_ma13'] = df_relevant['ai_bubble'].rolling(window=13).mean()  # 3-month MA

# Volatility and stability analysis
print("\n" + "="*80)
print("5. VOLATILITY & STABILITY ANALYSIS")
print("="*80)

# Calculate coefficient of variation for each period
periods = {
    '2023': df['2023-01-01':'2023-12-31']['ai_bubble'],
    '2024': df['2024-01-01':'2024-12-31']['ai_bubble'],
    '2025': df['2025-01-01':'2025-12-31']['ai_bubble'],
    'Last 3 months': df_relevant['ai_bubble'][-13:],
}

print("\nVolatility Analysis (Coefficient of Variation):")
for period_name, data in periods.items():
    if len(data) > 0 and data.mean() > 0:
        cv = (data.std() / data.mean()) * 100
        stability = "Stable" if cv < 50 else "Moderate" if cv < 100 else "Highly Volatile"
        print(f"  {period_name}: {cv:.1f}% - {stability}")

# Correlation with real AI development metrics
print("\n" + "="*80)
print("6. BUBBLE vs REALITY CHECK (Post-2023 Correlations)")
print("="*80)

# Create composite indices
df_relevant['technical_index'] = df_relevant[['prompt_engineering', 'langchain', 'ai_roadmap']].mean(axis=1)
df_relevant['hype_index'] = (df_relevant['ai_bubble'] + df_relevant['ai_startup']) / 2

# Calculate correlations
correlations = {
    'Bubble vs Technical Development': df_relevant['ai_bubble'].corr(df_relevant['technical_index']),
    'Bubble vs Startup Activity': df_relevant['ai_bubble'].corr(df_relevant['ai_startup']),
    'Bubble vs Prompt Engineering': df_relevant['ai_bubble'].corr(df_relevant['prompt_engineering']),
}

print("\nCorrelation Analysis:")
for metric, corr in correlations.items():
    strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.4 else "Weak"
    print(f"  {metric}: {corr:.3f} ({strength})")

# Divergence Analysis
print("\n" + "="*80)
print("7. DIVERGENCE ANALYSIS: HYPE vs FUNDAMENTALS")
print("="*80)

# Compare growth rates over different periods
periods_growth = [
    ('Last 3 months', -13),
    ('Last 6 months', -26),
    ('Since GPT-4', df_relevant.index.get_loc(df_relevant['2023-03-01':].index[0]) - len(df_relevant))
]

for period_name, offset in periods_growth:
    if abs(offset) < len(df_relevant):
        bubble_start = df_relevant['ai_bubble'].iloc[offset] if offset < 0 else df_relevant['ai_bubble'].iloc[0]
        tech_start = df_relevant['technical_index'].iloc[offset] if offset < 0 else df_relevant['technical_index'].iloc[0]

        if bubble_start > 0 and tech_start > 0:
            bubble_growth = ((df_relevant['ai_bubble'].iloc[-1] / bubble_start) - 1) * 100
            tech_growth = ((df_relevant['technical_index'].iloc[-1] / tech_start) - 1) * 100
            divergence = bubble_growth - tech_growth

            print(f"\n{period_name}:")
            print(f"  - Bubble concern growth: {bubble_growth:.1f}%")
            print(f"  - Technical growth: {tech_growth:.1f}%")
            print(f"  - Divergence: {divergence:+.1f}%")
            if divergence > 50:
                print(f"  - ⚠️ WARNING: Significant divergence detected!")

# Pattern Recognition
print("\n" + "="*80)
print("8. PATTERN RECOGNITION & BUBBLE INDICATORS")
print("="*80)

# Calculate key bubble indicators
current_value = df_relevant['ai_bubble'].iloc[-1]
peak_value = df_relevant['ai_bubble'].max()
avg_2024 = df['2024-01-01':'2024-12-31']['ai_bubble'].mean()
avg_2025 = df['2025-01-01':'2025-12-31']['ai_bubble'].mean()

bubble_indicators = {
    'Exponential Growth': avg_2025 / avg_2024 > 2 if avg_2024 > 0 else False,
    'Near Peak Values': current_value > peak_value * 0.8,
    'Sustained High Level': df_relevant['ai_bubble'][-4:].mean() > 20,
    'Divergence from Fundamentals': df_relevant['ai_bubble'].iloc[-1] > df_relevant['technical_index'].iloc[-1] * 2,
    'Increasing Volatility': df_relevant['ai_bubble'][-13:].std() > df_relevant['ai_bubble'][-52:].std() if len(df_relevant) > 52 else False,
}

print("\nBubble Indicator Checklist:")
bubble_score = 0
for indicator, is_present in bubble_indicators.items():
    status = "✅" if is_present else "❌"
    print(f"  {status} {indicator}")
    if is_present:
        bubble_score += 20

# Predictive Analysis
print("\n" + "="*80)
print("9. PREDICTIVE ANALYSIS")
print("="*80)

# Simple trend projection based on recent momentum
recent_weeks = 8
if len(df_relevant) >= recent_weeks:
    recent_trend = df_relevant['ai_bubble'][-recent_weeks:]
    weekly_change = recent_trend.diff().mean()

    # Project next 4 weeks
    print(f"\nBased on {recent_weeks}-week trend:")
    print(f"  - Average weekly change: {weekly_change:+.2f}")
    print(f"  - Current value: {current_value:.0f}")
    print(f"  - 4-week projection: {current_value + (weekly_change * 4):.0f}")

    # Momentum indicators
    momentum_increasing = recent_trend.diff().iloc[-1] > recent_trend.diff().iloc[-4] if len(recent_trend) > 4 else False
    print(f"  - Momentum: {'Accelerating ⚡' if momentum_increasing else 'Stabilizing 📊'}")

# Calculate probability scores
print("\n" + "="*80)
print("10. FINAL PROBABILITY ASSESSMENT")
print("="*80)

# Are we in a bubble?
bubble_probability = bubble_score

# Will searches increase?
increase_factors = {
    'Positive momentum': weekly_change > 0,
    'Below historical peak': current_value < peak_value,
    'Technical growth continues': df_relevant['technical_index'].iloc[-1] > df_relevant['technical_index'].iloc[-13],
    'Recent acceleration': df_relevant['ai_bubble'].iloc[-1] > df_relevant['ai_bubble'].iloc[-4],
    'Startup activity rising': df_relevant['ai_startup'].iloc[-1] > df_relevant['ai_startup'].iloc[-13],
}

increase_probability = sum(20 for factor, is_true in increase_factors.items() if is_true)

print(f"\n🎯 BUBBLE PROBABILITY: {bubble_probability}%")
print(f"📈 SEARCH INCREASE PROBABILITY: {increase_probability}%")

# Final Verdict
print("\n" + "="*80)
print("FINAL VERDICT - DATA-DRIVEN CONCLUSION")
print("="*80)

print(f"""
Based on refined analysis of post-2023 Google Trends data:

1. **AI BUBBLE STATUS:**
   Probability: {bubble_probability}%

   The data shows a {avg_2025/avg_2024:.1f}x increase from 2024 to 2025 average.
   Current search volume ({current_value}) represents a dramatic escalation in bubble concerns.
   We are {'DEFINITELY' if bubble_probability >= 80 else 'LIKELY' if bubble_probability >= 60 else 'POSSIBLY'} in an AI bubble awareness phase.

2. **FUTURE TREND PROJECTION:**
   Probability of Increase: {increase_probability}%

   Recent momentum suggests searches will {'likely CONTINUE TO RISE' if increase_probability >= 60 else 'potentially STABILIZE'}.
   The 8-week trend shows {'+' if weekly_change > 0 else ''}{weekly_change:.1f} points/week average change.

3. **KEY FINDINGS:**
   • Peak "AI bubble" searches reached {peak_value} (week of {df_relevant['ai_bubble'].idxmax().date()})
   • Bubble concerns are growing {(avg_2025/avg_2024-1)*100:.0f}% faster than in 2024
   • {'⚠️ CRITICAL: Significant divergence between bubble fears and technical fundamentals' if bubble_probability >= 80 else '📊 Bubble concerns tracking with broader AI development'}

4. **CONFIDENCE LEVEL:** {'HIGH' if bubble_probability >= 70 and increase_probability >= 70 else 'MODERATE' if bubble_probability >= 50 or increase_probability >= 50 else 'LOW'}

CONCLUSION: We are {
'DEFINITIVELY experiencing an AI bubble phenomenon with strong likelihood of continued growth in bubble concerns.'
if bubble_probability >= 80 and increase_probability >= 60 else
'LIKELY in an AI bubble awareness phase with probable continued growth in concerns.'
if bubble_probability >= 60 else
'seeing ELEVATED bubble concerns but not yet at critical bubble levels.'}
""")

# Create comprehensive visualizations
fig = plt.figure(figsize=(16, 12))

# Layout: 3x3 grid
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Main trend with phases
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(df_relevant.index, df_relevant['ai_bubble'], 'r-', linewidth=2, label='AI Bubble')
ax1.plot(df_relevant.index, df_relevant['ai_bubble_ma13'], 'r--', alpha=0.7, label='3-month MA')
ax1.fill_between(df_relevant.index, 0, df_relevant['ai_bubble'], alpha=0.2, color='red')
ax1.set_title('AI Bubble Search Trend (2023-2025) - Post ChatGPT Era', fontsize=14, fontweight='bold')
ax1.set_ylabel('Search Interest')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add phase annotations
ax1.axvspan('2023-01-01', '2023-06-01', alpha=0.1, color='yellow', label='Early Awareness')
ax1.axvspan('2025-05-01', df_relevant.index[-1], alpha=0.1, color='red', label='Surge Period')

# 2. Monthly aggregation
ax2 = fig.add_subplot(gs[1, 0])
ax2.bar(df_monthly.index, df_monthly['ai_bubble'], color='red', alpha=0.7)
ax2.set_title('Monthly Average - AI Bubble Searches')
ax2.set_ylabel('Average Search Interest')
ax2.tick_params(axis='x', rotation=45)

# 3. Bubble vs Technical Index
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(df_relevant.index, df_relevant['ai_bubble'], 'r-', label='Bubble Concerns', linewidth=2)
ax3.plot(df_relevant.index, df_relevant['technical_index'], 'b-', label='Technical Development', linewidth=2)
ax3.set_title('Bubble Concerns vs Technical Reality')
ax3.set_ylabel('Search Interest')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Growth comparison
ax4 = fig.add_subplot(gs[1, 2])
categories = ['AI Bubble', 'Technical', 'Startups']
growth_values = [
    ((df_relevant['ai_bubble'].iloc[-1] / df_relevant['ai_bubble'].iloc[-26]) - 1) * 100 if df_relevant['ai_bubble'].iloc[-26] > 0 else 0,
    ((df_relevant['technical_index'].iloc[-1] / df_relevant['technical_index'].iloc[-26]) - 1) * 100 if df_relevant['technical_index'].iloc[-26] > 0 else 0,
    ((df_relevant['ai_startup'].iloc[-1] / df_relevant['ai_startup'].iloc[-26]) - 1) * 100 if df_relevant['ai_startup'].iloc[-26] > 0 else 0,
]
colors = ['red', 'blue', 'green']
bars = ax4.bar(categories, growth_values, color=colors, alpha=0.7)
ax4.set_title('6-Month Growth Comparison')
ax4.set_ylabel('Growth %')
ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
for bar, val in zip(bars, growth_values):
    ax4.text(bar.get_x() + bar.get_width()/2, val + 5, f'{val:.0f}%', ha='center')

# 5. Quarterly progression
ax5 = fig.add_subplot(gs[2, 0])
ax5.plot(df_quarterly.index, df_quarterly['ai_bubble'], 'ro-', linewidth=2, markersize=8)
ax5.set_title('Quarterly Average Progression')
ax5.set_ylabel('Average Search Interest')
ax5.grid(True, alpha=0.3)
ax5.tick_params(axis='x', rotation=45)

# 6. Recent zoom (2025)
ax6 = fig.add_subplot(gs[2, 1])
df_2025 = df['2025-01-01':'2025-12-31']
ax6.plot(df_2025.index, df_2025['ai_bubble'], 'r-', linewidth=2, marker='o', markersize=4)
ax6.fill_between(df_2025.index, 0, df_2025['ai_bubble'], alpha=0.3, color='red')
ax6.set_title('2025 Detail - The Surge', fontweight='bold')
ax6.set_ylabel('Search Interest')
ax6.grid(True, alpha=0.3)
ax6.tick_params(axis='x', rotation=45)

# 7. Probability meters
ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')
# Create text-based probability display
prob_text = f"""Probability Assessment

🎯 AI Bubble
{bubble_probability}%
{'█' * int(bubble_probability/5)}

📈 Trend Increase
{increase_probability}%
{'█' * int(increase_probability/5)}

Status: {'🔴 HIGH ALERT' if bubble_probability >= 80 else '🟡 CAUTION' if bubble_probability >= 60 else '🟢 MONITORING'}
"""
ax7.text(0.5, 0.5, prob_text, fontsize=10, ha='center', va='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('AI Bubble Analysis - Comprehensive Dashboard', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('ai_bubble_refined_analysis.png', dpi=150, bbox_inches='tight')
print("\n📊 Enhanced visualization saved as 'ai_bubble_refined_analysis.png'")

# Don't show() to prevent hanging
# plt.show()