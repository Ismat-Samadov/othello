#!/usr/bin/env python3
"""
Script to create visualizations from Azerbaijan population data
and save them to the charts folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

# Set the font to support Unicode characters
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# Create charts directory
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

# Set style for better-looking charts
plt.style.use('seaborn-v0_8-darkgrid')


def clean_numeric(value):
    """Convert comma-separated numbers to float."""
    if isinstance(value, str):
        return float(value.replace(',', '.'))
    return value


def create_population_trends_chart():
    """Create chart showing total population trends over time."""
    print("Creating population trends chart...")

    # Read data
    df = pd.read_csv('population_tables/table_1_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)

    # Clean column names and data
    df.columns = ['Year', 'Total', 'Urban', 'Rural', 'Urban_Pct', 'Rural_Pct']

    # Convert numbers
    for col in ['Total', 'Urban', 'Rural']:
        df[col] = df[col].apply(clean_numeric)

    df['Year'] = df['Year'].astype(int)

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(df['Year'], df['Total'], marker='o', linewidth=2.5,
            label='Total Population', color='#2E86AB', markersize=4)
    ax.plot(df['Year'], df['Urban'], marker='s', linewidth=2,
            label='Urban Population', color='#A23B72', markersize=3)
    ax.plot(df['Year'], df['Rural'], marker='^', linewidth=2,
            label='Rural Population', color='#F18F01', markersize=3)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population (thousands)', fontsize=12, fontweight='bold')
    ax.set_title('Azerbaijan Population Trends (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/01_population_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/01_population_trends.png")


def create_urban_rural_distribution():
    """Create stacked area chart showing urban vs rural distribution."""
    print("Creating urban-rural distribution chart...")

    df = pd.read_csv('population_tables/table_1_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Total', 'Urban', 'Rural', 'Urban_Pct', 'Rural_Pct']

    for col in ['Urban', 'Rural']:
        df[col] = df[col].apply(clean_numeric)
    df['Year'] = df['Year'].astype(int)

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))

    ax.fill_between(df['Year'], 0, df['Urban'], alpha=0.7,
                     label='Urban', color='#A23B72')
    ax.fill_between(df['Year'], df['Urban'], df['Urban'] + df['Rural'],
                     alpha=0.7, label='Rural', color='#F18F01')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population (thousands)', fontsize=12, fontweight='bold')
    ax.set_title('Urban vs Rural Population Distribution (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/02_urban_rural_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/02_urban_rural_distribution.png")


def create_urbanization_rate_chart():
    """Create chart showing urbanization rate over time."""
    print("Creating urbanization rate chart...")

    df = pd.read_csv('population_tables/table_1_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Total', 'Urban', 'Rural', 'Urban_Pct', 'Rural_Pct']

    df['Urban_Pct'] = df['Urban_Pct'].apply(clean_numeric)
    df['Year'] = df['Year'].astype(int)

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(df['Year'], df['Urban_Pct'], marker='o', linewidth=2.5,
            color='#2E86AB', markersize=5)
    ax.fill_between(df['Year'], 50, df['Urban_Pct'], alpha=0.3, color='#2E86AB')
    ax.axhline(y=50, color='red', linestyle='--', linewidth=1, alpha=0.5, label='50% threshold')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Urban Population (%)', fontsize=12, fontweight='bold')
    ax.set_title('Urbanization Rate in Azerbaijan (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([45, 56])

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/03_urbanization_rate.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/03_urbanization_rate.png")


def create_birth_death_chart():
    """Create chart showing birth and death rates."""
    print("Creating birth and death rates chart...")

    df = pd.read_csv('population_tables/table_2_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Births_Num', 'Deaths_Num', 'Natural_Inc',
                  'Births_Rate', 'Deaths_Rate', 'Natural_Inc_Rate']

    for col in ['Births_Rate', 'Deaths_Rate', 'Natural_Inc_Rate']:
        df[col] = df[col].apply(clean_numeric)
    df['Year'] = df['Year'].astype(int)

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(df['Year'], df['Births_Rate'], marker='o', linewidth=2.5,
            label='Birth Rate', color='#06A77D', markersize=4)
    ax.plot(df['Year'], df['Deaths_Rate'], marker='s', linewidth=2.5,
            label='Death Rate', color='#D62828', markersize=4)
    ax.plot(df['Year'], df['Natural_Inc_Rate'], marker='^', linewidth=2.5,
            label='Natural Increase', color='#2E86AB', markersize=4)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Rate (per 1,000 population)', fontsize=12, fontweight='bold')
    ax.set_title('Birth and Death Rates in Azerbaijan (2000-2024)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/04_birth_death_rates.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/04_birth_death_rates.png")


def create_natural_increase_chart():
    """Create chart showing absolute numbers of births, deaths, and natural increase."""
    print("Creating natural increase chart...")

    df = pd.read_csv('population_tables/table_2_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Births_Num', 'Deaths_Num', 'Natural_Inc',
                  'Births_Rate', 'Deaths_Rate', 'Natural_Inc_Rate']

    df['Year'] = df['Year'].astype(int)

    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(df['Year']))
    width = 0.35

    bars1 = ax.bar(x - width/2, df['Births_Num'], width,
                   label='Births', color='#06A77D', alpha=0.8)
    bars2 = ax.bar(x + width/2, df['Deaths_Num'], width,
                   label='Deaths', color='#D62828', alpha=0.8)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of People', fontsize=12, fontweight='bold')
    ax.set_title('Births vs Deaths in Azerbaijan (2000-2024)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x[::2])
    ax.set_xticklabels(df['Year'][::2], rotation=45)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/05_births_vs_deaths.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/05_births_vs_deaths.png")


def create_age_distribution_chart():
    """Create chart showing age distribution for recent years."""
    print("Creating age distribution chart...")

    df = pd.read_csv('population_tables/table_3_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)

    # Extract age groups (skip first two rows which are headers/totals)
    df = df.iloc[2:]

    age_groups = df.iloc[:, 0].tolist()
    pop_2025 = df.iloc[:, 5].apply(clean_numeric).tolist()

    fig, ax = plt.subplots(figsize=(14, 8))

    colors = plt.cm.viridis(np.linspace(0, 1, len(age_groups)))
    bars = ax.barh(age_groups, pop_2025, color=colors, alpha=0.8)

    ax.set_xlabel('Population (thousands)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Age Groups', fontsize=12, fontweight='bold')
    ax.set_title('Population Distribution by Age Groups (2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/06_age_distribution_2025.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/06_age_distribution_2025.png")


def create_age_trends_chart():
    """Create chart showing how age distribution changes over years."""
    print("Creating age trends chart...")

    df = pd.read_csv('population_tables/table_3_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)

    # Extract data (skip first two rows)
    df = df.iloc[2:]

    age_groups = df.iloc[:, 0].tolist()
    years = ['2020', '2021', '2022', '2023', '2024', '2025']

    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot lines for each age group
    colors = plt.cm.tab20(np.linspace(0, 1, len(age_groups)))

    for idx, age_group in enumerate(age_groups):
        values = [clean_numeric(df.iloc[idx, i]) for i in range(1, 7)]
        ax.plot(years, values, marker='o', label=age_group,
                color=colors[idx], linewidth=2, markersize=4)

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Population (thousands)', fontsize=12, fontweight='bold')
    ax.set_title('Population Trends by Age Groups (2020-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=8, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/07_age_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/07_age_trends.png")


def create_marriages_divorces_chart():
    """Create chart showing marriages and divorces trends."""
    print("Creating marriages and divorces chart...")

    df = pd.read_csv('population_tables/table_4_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Marriages_Num', 'Divorces_Num', 'Marriages_Rate', 'Divorces_Rate']

    df['Year'] = df['Year'].astype(int)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

    # Chart 1: Absolute numbers
    ax1.plot(df['Year'], df['Marriages_Num'], marker='o', linewidth=2.5,
             label='Marriages', color='#06A77D', markersize=4)
    ax1.plot(df['Year'], df['Divorces_Num'], marker='s', linewidth=2.5,
             label='Divorces', color='#D62828', markersize=4)

    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number', fontsize=12, fontweight='bold')
    ax1.set_title('Marriages and Divorces in Azerbaijan (2000-2024)',
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Chart 2: Rates per 1000 population
    for col in ['Marriages_Rate', 'Divorces_Rate']:
        df[col] = df[col].apply(clean_numeric)

    ax2.plot(df['Year'], df['Marriages_Rate'], marker='o', linewidth=2.5,
             label='Marriage Rate', color='#06A77D', markersize=4)
    ax2.plot(df['Year'], df['Divorces_Rate'], marker='s', linewidth=2.5,
             label='Divorce Rate', color='#D62828', markersize=4)

    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Rate (per 1,000 population)', fontsize=12, fontweight='bold')
    ax2.set_title('Marriage and Divorce Rates per 1,000 Population',
                  fontsize=16, fontweight='bold', pad=20)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/08_marriages_divorces.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/08_marriages_divorces.png")


def create_divorce_marriage_ratio_chart():
    """Create chart showing divorce to marriage ratio."""
    print("Creating divorce-to-marriage ratio chart...")

    df = pd.read_csv('population_tables/table_4_Azərbaycan_Respublikasının_əhalisi.csv',
                     skiprows=1)
    df.columns = ['Year', 'Marriages_Num', 'Divorces_Num', 'Marriages_Rate', 'Divorces_Rate']

    df['Year'] = df['Year'].astype(int)
    df['Ratio'] = (df['Divorces_Num'] / df['Marriages_Num'] * 100)

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.plot(df['Year'], df['Ratio'], marker='o', linewidth=2.5,
            color='#D62828', markersize=5)
    ax.fill_between(df['Year'], 0, df['Ratio'], alpha=0.3, color='#D62828')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Divorce-to-Marriage Ratio (%)', fontsize=12, fontweight='bold')
    ax.set_title('Divorce-to-Marriage Ratio in Azerbaijan (2000-2024)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/09_divorce_marriage_ratio.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {CHARTS_DIR}/09_divorce_marriage_ratio.png")


def main():
    """Generate all charts."""
    print("Starting chart generation...\n")

    create_population_trends_chart()
    create_urban_rural_distribution()
    create_urbanization_rate_chart()
    create_birth_death_chart()
    create_natural_increase_chart()
    create_age_distribution_chart()
    create_age_trends_chart()
    create_marriages_divorces_chart()
    create_divorce_marriage_ratio_chart()

    print(f"\nAll charts have been saved to the '{CHARTS_DIR}/' directory!")
    print(f"Total charts created: 9")


if __name__ == "__main__":
    main()
