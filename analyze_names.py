#!/usr/bin/env python3
"""
数据分析脚本：美国婴儿姓名趋势分析
分析names_all_years.csv数据集，探索姓名趋势、性别差异和社会变化
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_and_explore_data():
    """加载和探索数据"""
    print("正在加载数据...")
    df = pd.read_csv('names_all_years.csv')
    
    print(f"数据集形状: {df.shape}")
    print(f"列名: {df.columns.tolist()}")
    print(f"数据类型:\n{df.dtypes}")
    print(f"缺失值:\n{df.isnull().sum()}")
    print(f"年份范围: {df['Year'].min()} - {df['Year'].max()}")
    print(f"性别分布:\n{df['Gender'].value_counts()}")
    
    return df

def basic_statistics(df):
    """基本统计分析"""
    print("\n=== 基本统计分析 ===")
    
    # 总记录数
    total_records = len(df)
    print(f"总记录数: {total_records:,}")
    
    # 年份统计
    year_stats = df.groupby('Year').agg({
        'Count': 'sum',
        'Name': 'nunique'
    }).reset_index()
    year_stats.columns = ['Year', 'Total_Births', 'Unique_Names']
    
    print(f"年份范围: {df['Year'].min()} - {df['Year'].max()}")
    print(f"总出生人数: {df['Count'].sum():,}")
    print(f"唯一姓名数: {df['Name'].nunique():,}")
    
    return year_stats

def analyze_name_trends(df):
    """分析姓名趋势"""
    print("\n=== 姓名趋势分析 ===")
    
    # 按年份和性别分组
    yearly_gender = df.groupby(['Year', 'Gender'])['Count'].sum().unstack(fill_value=0)
    
    # 计算每年总出生数
    yearly_total = df.groupby('Year')['Count'].sum()
    
    # 分析最受欢迎的姓名
    top_names_all_time = df.groupby('Name')['Count'].sum().sort_values(ascending=False).head(10)
    print("历史上最受欢迎的10个姓名:")
    for name, count in top_names_all_time.items():
        print(f"{name}: {count:,}")
    
    return yearly_gender, yearly_total, top_names_all_time

def analyze_gender_patterns(df):
    """分析性别模式"""
    print("\n=== 性别模式分析 ===")
    
    # 按性别统计
    gender_stats = df.groupby('Gender').agg({
        'Count': 'sum',
        'Name': 'nunique'
    })
    print("按性别统计:")
    print(gender_stats)
    
    # 分析性别比例变化
    yearly_gender_ratio = df.groupby(['Year', 'Gender'])['Count'].sum().unstack(fill_value=0)
    yearly_gender_ratio['F_ratio'] = yearly_gender_ratio['F'] / (yearly_gender_ratio['F'] + yearly_gender_ratio['M'])
    yearly_gender_ratio['M_ratio'] = yearly_gender_ratio['M'] / (yearly_gender_ratio['F'] + yearly_gender_ratio['M'])
    
    return yearly_gender_ratio

def analyze_name_diversity(df):
    """分析姓名多样性"""
    print("\n=== 姓名多样性分析 ===")
    
    # 计算每年的姓名多样性（唯一姓名数）
    yearly_diversity = df.groupby('Year')['Name'].nunique()
    
    # 计算每年的集中度（前10名姓名的占比）
    yearly_top10_share = []
    for year in df['Year'].unique():
        year_data = df[df['Year'] == year]
        total_births = year_data['Count'].sum()
        top10_births = year_data.nlargest(10, 'Count')['Count'].sum()
        share = top10_births / total_births
        yearly_top10_share.append({'Year': year, 'Top10_Share': share})
    
    diversity_df = pd.DataFrame(yearly_top10_share)
    
    print(f"姓名多样性变化: {yearly_diversity.min():,} - {yearly_diversity.max():,}")
    print(f"前10名姓名占比变化: {diversity_df['Top10_Share'].min():.3f} - {diversity_df['Top10_Share'].max():.3f}")
    
    return yearly_diversity, diversity_df

def create_visualizations(df, yearly_gender, yearly_total, top_names_all_time, yearly_gender_ratio, yearly_diversity, diversity_df):
    """创建可视化图表"""
    print("\n=== 创建可视化图表 ===")
    
    # 设置图表样式
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(20, 15))
    
    # 1. 年度出生人数趋势
    ax1 = plt.subplot(3, 3, 1)
    yearly_total.plot(ax=ax1, color='steelblue', linewidth=2)
    ax1.set_title('年度出生人数趋势 (1880-2023)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('年份')
    ax1.set_ylabel('出生人数')
    ax1.grid(True, alpha=0.3)
    
    # 2. 性别分布变化
    ax2 = plt.subplot(3, 3, 2)
    yearly_gender_ratio[['F_ratio', 'M_ratio']].plot(ax=ax2, color=['pink', 'lightblue'], linewidth=2)
    ax2.set_title('性别比例变化趋势', fontsize=14, fontweight='bold')
    ax2.set_xlabel('年份')
    ax2.set_ylabel('比例')
    ax2.legend(['女性', '男性'])
    ax2.grid(True, alpha=0.3)
    
    # 3. 姓名多样性变化
    ax3 = plt.subplot(3, 3, 3)
    yearly_diversity.plot(ax=ax3, color='green', linewidth=2)
    ax3.set_title('年度唯一姓名数量变化', fontsize=14, fontweight='bold')
    ax3.set_xlabel('年份')
    ax3.set_ylabel('唯一姓名数')
    ax3.grid(True, alpha=0.3)
    
    # 4. 前10名姓名占比变化
    ax4 = plt.subplot(3, 3, 4)
    diversity_df.set_index('Year')['Top10_Share'].plot(ax=ax4, color='red', linewidth=2)
    ax4.set_title('前10名姓名占比变化', fontsize=14, fontweight='bold')
    ax4.set_xlabel('年份')
    ax4.set_ylabel('占比')
    ax4.grid(True, alpha=0.3)
    
    # 5. 历史上最受欢迎的姓名
    ax5 = plt.subplot(3, 3, 5)
    top_names_all_time.head(10).plot(kind='barh', ax=ax5, color='purple')
    ax5.set_title('历史上最受欢迎的10个姓名', fontsize=14, fontweight='bold')
    ax5.set_xlabel('总出生人数')
    
    # 6. 按性别的最受欢迎姓名
    ax6 = plt.subplot(3, 3, 6)
    top_female = df[df['Gender'] == 'F'].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    top_male = df[df['Gender'] == 'M'].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    
    y_pos = np.arange(len(top_female))
    ax6.barh(y_pos, top_female.values, color='pink', alpha=0.7, label='女性')
    ax6.set_yticks(y_pos)
    ax6.set_yticklabels(top_female.index)
    ax6.set_title('最受欢迎的女性姓名', fontsize=14, fontweight='bold')
    ax6.set_xlabel('总出生人数')
    
    # 7. 最受欢迎的男性姓名
    ax7 = plt.subplot(3, 3, 7)
    y_pos = np.arange(len(top_male))
    ax7.barh(y_pos, top_male.values, color='lightblue', alpha=0.7)
    ax7.set_yticks(y_pos)
    ax7.set_yticklabels(top_male.index)
    ax7.set_title('最受欢迎的男性姓名', fontsize=14, fontweight='bold')
    ax7.set_xlabel('总出生人数')
    
    # 8. 姓名长度分布
    ax8 = plt.subplot(3, 3, 8)
    df['Name_Length'] = df['Name'].str.len()
    length_dist = df.groupby('Name_Length')['Count'].sum()
    length_dist.plot(kind='bar', ax=ax8, color='orange')
    ax8.set_title('姓名长度分布', fontsize=14, fontweight='bold')
    ax8.set_xlabel('姓名长度')
    ax8.set_ylabel('总出生人数')
    
    # 9. 现代vs传统姓名对比（以2000年为分界点）
    ax9 = plt.subplot(3, 3, 9)
    traditional = df[df['Year'] < 2000].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    modern = df[df['Year'] >= 2000].groupby('Name')['Count'].sum().sort_values(ascending=False).head(5)
    
    # 创建对比图
    x = np.arange(len(traditional))
    width = 0.35
    
    ax9.bar(x - width/2, traditional.values, width, label='传统时期 (<2000)', color='brown', alpha=0.7)
    ax9.bar(x + width/2, modern.values, width, label='现代时期 (≥2000)', color='cyan', alpha=0.7)
    
    ax9.set_xlabel('排名')
    ax9.set_ylabel('总出生人数')
    ax9.set_title('传统vs现代最受欢迎姓名对比', fontsize=14, fontweight='bold')
    ax9.set_xticks(x)
    ax9.set_xticklabels(range(1, 6))
    ax9.legend()
    
    plt.tight_layout()
    plt.savefig('name_analysis_visualizations.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def analyze_modern_trends(df):
    """分析现代趋势（2000年后）"""
    print("\n=== 现代趋势分析 (2000年后) ===")
    
    modern_df = df[df['Year'] >= 2000]
    
    # 现代最受欢迎的姓名
    modern_top = modern_df.groupby('Name')['Count'].sum().sort_values(ascending=False).head(10)
    print("2000年后最受欢迎的10个姓名:")
    for name, count in modern_top.items():
        print(f"{name}: {count:,}")
    
    # 分析新兴姓名（在2000年前很少出现，2000年后很受欢迎）
    pre_2000 = df[df['Year'] < 2000]
    post_2000 = df[df['Year'] >= 2000]
    
    pre_2000_totals = pre_2000.groupby('Name')['Count'].sum()
    post_2000_totals = post_2000.groupby('Name')['Count'].sum()
    
    # 找出新兴姓名（2000年前很少，2000年后很多）
    emerging_names = []
    for name in post_2000_totals.index:
        pre_count = pre_2000_totals.get(name, 0)
        post_count = post_2000_totals[name]
        if pre_count < 1000 and post_count > 10000:  # 阈值可调整
            emerging_names.append((name, pre_count, post_count))
    
    emerging_names.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n新兴姓名（2000年前<1000人，2000年后>10000人）:")
    for name, pre, post in emerging_names[:10]:
        print(f"{name}: {pre} -> {post:,}")
    
    return modern_top, emerging_names

def main():
    """主函数"""
    print("=== 美国婴儿姓名趋势分析 ===")
    print("分析names_all_years.csv数据集\n")
    
    # 加载数据
    df = load_and_explore_data()
    
    # 基本统计
    year_stats = basic_statistics(df)
    
    # 姓名趋势分析
    yearly_gender, yearly_total, top_names_all_time = analyze_name_trends(df)
    
    # 性别模式分析
    yearly_gender_ratio = analyze_gender_patterns(df)
    
    # 姓名多样性分析
    yearly_diversity, diversity_df = analyze_name_diversity(df)
    
    # 现代趋势分析
    modern_top, emerging_names = analyze_modern_trends(df)
    
    # 创建可视化
    fig = create_visualizations(df, yearly_gender, yearly_total, top_names_all_time, 
                               yearly_gender_ratio, yearly_diversity, diversity_df)
    
    print("\n=== 分析完成 ===")
    print("可视化图表已保存为 'name_analysis_visualizations.png'")
    
    return df, year_stats, yearly_gender, yearly_total, top_names_all_time, yearly_gender_ratio, yearly_diversity, diversity_df, modern_top, emerging_names

if __name__ == "__main__":
    results = main()
