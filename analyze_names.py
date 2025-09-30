#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_and_explore_data():
    print("Loading data...")
    df = pd.read_csv('names_all_years.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Data types:\n{df.dtypes}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Gender distribution:\n{df['Gender'].value_counts()}")
    
    return df

def basic_statistics(df):
    print("\n=== Basic Statistical Analysis ===")
    
    total_records = len(df)
    print(f"Total records: {total_records:,}")
    
    year_stats = df.groupby('Year').agg({
        'Count': 'sum',
        'Name': 'nunique'
    }).reset_index()
    year_stats.columns = ['Year', 'Total_Births', 'Unique_Names']
    
    print(f"Year range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Total births: {df['Count'].sum():,}")
    print(f"Unique names: {df['Name'].nunique():,}")
    
    return year_stats

def analyze_name_trends(df):
    print("\n=== Name Trends Analysis ===")
    
    yearly_gender = df.groupby(['Year', 'Gender'])['Count'].sum().unstack(fill_value=0)
    yearly_total = df.groupby('Year')['Count'].sum()
    
    top_names_all_time = df.groupby('Name')['Count'].sum().sort_values(ascending=False).head(10)
    print("Top 10 most popular names of all time:")
    for name, count in top_names_all_time.items():
        print(f"{name}: {count:,}")
    
    return yearly_gender, yearly_total, top_names_all_time

def analyze_gender_patterns(df):
    print("\n=== Gender Patterns Analysis ===")
    
    gender_stats = df.groupby('Gender').agg({
        'Count': 'sum',
        'Name': 'nunique'
    })
    print("Statistics by gender:")
    print(gender_stats)
    
    yearly_gender_ratio = df.groupby(['Year', 'Gender'])['Count'].sum().unstack(fill_value=0)
    yearly_gender_ratio['F_ratio'] = yearly_gender_ratio['F'] / (yearly_gender_ratio['F'] + yearly_gender_ratio['M'])
    yearly_gender_ratio['M_ratio'] = yearly_gender_ratio['M'] / (yearly_gender_ratio['F'] + yearly_gender_ratio['M'])
    
    return yearly_gender_ratio

def analyze_name_diversity(df):
    print("\n=== Name Diversity Analysis ===")
    
    yearly_diversity = df.groupby('Year')['Name'].nunique()
    
    yearly_top10_share = []
    for year in df['Year'].unique():
        year_data = df[df['Year'] == year]
        total_births = year_data['Count'].sum()
        top10_births = year_data.nlargest(10, 'Count')['Count'].sum()
        share = top10_births / total_births
        yearly_top10_share.append({'Year': year, 'Top10_Share': share})
    
    diversity_df = pd.DataFrame(yearly_top10_share)
    
    print(f"Name diversity range: {yearly_diversity.min():,} - {yearly_diversity.max():,}")
    print(f"Top 10 names share range: {diversity_df['Top10_Share'].min():.3f} - {diversity_df['Top10_Share'].max():.3f}")
    
    return yearly_diversity, diversity_df

def create_visualizations(df, yearly_gender, yearly_total, top_names_all_time, yearly_gender_ratio, yearly_diversity, diversity_df):
    print("\n=== Creating Visualization Charts ===")
    
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(20, 15))
    
    ax1 = plt.subplot(3, 3, 1)
    yearly_total.plot(ax=ax1, color='steelblue', linewidth=2)
    ax1.set_title('Annual Birth Trends (1880-2023)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Births')
    ax1.grid(True, alpha=0.3)
    
    ax2 = plt.subplot(3, 3, 2)
    yearly_gender_ratio[['F_ratio', 'M_ratio']].plot(ax=ax2, color=['pink', 'lightblue'], linewidth=2)
    ax2.set_title('Gender Ratio Changes Over Time', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Ratio')
    ax2.legend(['Female', 'Male'])
    ax2.grid(True, alpha=0.3)
    
    ax3 = plt.subplot(3, 3, 3)
    yearly_diversity.plot(ax=ax3, color='green', linewidth=2)
    ax3.set_title('Annual Unique Names Count Changes', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Number of Unique Names')
    ax3.grid(True, alpha=0.3)
    
    ax4 = plt.subplot(3, 3, 4)
    diversity_df.set_index('Year')['Top10_Share'].plot(ax=ax4, color='red', linewidth=2)
    ax4.set_title('Top 10 Names Share Changes', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Share')
    ax4.grid(True, alpha=0.3)
    
    ax5 = plt.subplot(3, 3, 5)
    top_names_all_time.head(10).plot(kind='barh', ax=ax5, color='purple')
    ax5.set_title('Most Popular Names of All Time', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Total Births')
    
    ax6 = plt.subplot(3, 3, 6)
    top_female = df[df['Gender'] == 'F'].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    top_male = df[df['Gender'] == 'M'].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    
    y_pos = np.arange(len(top_female))
    ax6.barh(y_pos, top_female.values, color='pink', alpha=0.7, label='Female')
    ax6.set_yticks(y_pos)
    ax6.set_yticklabels(top_female.index)
    ax6.set_title('Most Popular Female Names', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Total Births')
    
    ax7 = plt.subplot(3, 3, 7)
    y_pos = np.arange(len(top_male))
    ax7.barh(y_pos, top_male.values, color='lightblue', alpha=0.7)
    ax7.set_yticks(y_pos)
    ax7.set_yticklabels(top_male.index)
    ax7.set_title('Most Popular Male Names', fontsize=14, fontweight='bold')
    ax7.set_xlabel('Total Births')
    
    ax8 = plt.subplot(3, 3, 8)
    df['Name_Length'] = df['Name'].str.len()
    length_dist = df.groupby('Name_Length')['Count'].sum()
    length_dist.plot(kind='bar', ax=ax8, color='orange')
    ax8.set_title('Name Length Distribution', fontsize=14, fontweight='bold')
    ax8.set_xlabel('Name Length')
    ax8.set_ylabel('Total Births')
    
    ax9 = plt.subplot(3, 3, 9)
    traditional = df[df['Year'] < 2000].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    modern = df[df['Year'] >= 2000].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    
    x = np.arange(len(traditional))
    width = 0.35
    
    ax9.bar(x - width/2, traditional.values, width, label='Traditional Period (<2000)', color='brown', alpha=0.7)
    ax9.bar(x + width/2, modern.values, width, label='Modern Period (≥2000)', color='cyan', alpha=0.7)
    
    ax9.set_xlabel('Rank')
    ax9.set_ylabel('Total Births')
    ax9.set_title('Traditional vs Modern Most Popular Names Comparison', fontsize=14, fontweight='bold')
    ax9.set_xticks(x)
    ax9.set_xticklabels(range(1, 6))
    ax9.legend()
    
    plt.tight_layout()
    plt.savefig('name_analysis_visualizations.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def analyze_modern_trends(df):
    print("\n=== Modern Trends Analysis (After 2000) ===")
    
    modern_df = df[df['Year'] >= 2000]
    
    modern_top = modern_df.groupby('Name')['Count'].sum().sort_values(ascending=False).head(10)
    print("Top 10 most popular names after 2000:")
    for name, count in modern_top.items():
        print(f"{name}: {count:,}")
    
    pre_2000 = df[df['Year'] < 2000]
    post_2000 = df[df['Year'] >= 2000]
    
    pre_2000_totals = pre_2000.groupby('Name')['Count'].sum()
    post_2000_totals = post_2000.groupby('Name')['Count'].sum()
    
    emerging_names = []
    for name in post_2000_totals.index:
        pre_count = pre_2000_totals.get(name, 0)
        post_count = post_2000_totals[name]
        if pre_count < 1000 and post_count > 10000:
            emerging_names.append((name, pre_count, post_count))
    
    emerging_names.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\nEmerging names (rare before 2000, popular after 2000):")
    for name, pre, post in emerging_names[:10]:
        print(f"{name}: {pre} -> {post:,}")
    
    return modern_top, emerging_names

def main():
    print("=== US Baby Names Trend Analysis ===")
    print("Analyze names_all_years.csv dataset\n")
    
    df = load_and_explore_data()
    year_stats = basic_statistics(df)
    yearly_gender, yearly_total, top_names_all_time = analyze_name_trends(df)
    yearly_gender_ratio = analyze_gender_patterns(df)
    yearly_diversity, diversity_df = analyze_name_diversity(df)
    modern_top, emerging_names = analyze_modern_trends(df)
    
    fig = create_visualizations(df, yearly_gender, yearly_total, top_names_all_time, 
                               yearly_gender_ratio, yearly_diversity, diversity_df)
    
    print("\n=== Analysis Complete ===")
    print("Visualization charts saved as 'name_analysis_visualizations.png'")
    
    return df, year_stats, yearly_gender, yearly_total, top_names_all_time, yearly_gender_ratio, yearly_diversity, diversity_df, modern_top, emerging_names

if __name__ == "__main__":
    results = main()