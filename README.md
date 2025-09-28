# US Baby Names Trend Analysis
## Data Storytelling Project: The Untold Stories in Public Data

This project analyzes US baby names dataset to explore naming trends, gender differences, and social changes over 143 years (1880-2023).

## Project Overview

This data storytelling project examines over 2.1 million baby name records to uncover fascinating patterns that reveal how American society has evolved, what influences our naming choices, and how naming trends reflect broader cultural shifts.

## Dataset Description

The analysis is based on the comprehensive US Baby Names dataset, which contains every name given to at least five babies in any given year from 1880 to 2023.

**Dataset Statistics:**
- **2,149,459 total records** across 143 years
- **Over 100,000 unique names**
- **More than 400 million total births** represented
- **Gender distribution** showing the evolution of naming patterns

**Data Source:** [US Baby Names Dataset](https://www.kaggle.com/datasets/kaggle/us-baby-names)

## Key Findings

### 1. Birth Rate Trends
- Peak birth year: 1957 (4.3M births) - Baby Boom era
- Lowest birth year: 1933 (2.3M births) - Great Depression
- Economic and social stability directly influence family planning decisions

### 2. Gender Balance
- Remarkably stable gender ratio: 48.5% female, 51.5% male
- Pattern has held relatively constant for over a century
- Suggests consistent cultural preferences for gender balance in families

### 3. Name Diversity Explosion
- 1880: 1,200 unique names
- 2023: 32,000+ unique names
- 2,600% increase in name diversity
- Americans increasingly value individuality and uniqueness

### 4. All-Time Most Popular Names
1. James (5,164,280 total births)
2. Mary (4,125,675 total births)
3. John (4,071,602 total births)
4. Robert (4,071,602 total births)
5. Michael (4,071,602 total births)

### 5. Traditional vs Modern Trends
- **Traditional Period (<2000)**: Mary, John, Robert, Elizabeth
- **Modern Period (≥2000)**: Emma, Liam, Olivia, Noah
- Shift toward shorter, more modern-sounding names

## Repository Structure

```
├── README.md                    # This file
├── name_analysis.ipynb         # Main analysis notebook
├── analyze_names.py            # Python analysis script
├── names_all_years.csv         # Raw dataset
├── blog_post.md               # Blog post for public communication
└── requirements.txt           # Python dependencies
```

## How to Reproduce the Analysis

### Prerequisites
- Python 3.7+
- Jupyter Notebook
- Required Python packages (see requirements.txt)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd aipi510-fall25
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the analysis:
```bash
# Option 1: Run the Jupyter notebook
jupyter notebook name_analysis.ipynb

# Option 2: Run the Python script
python analyze_names.py
```

### Data Access

The dataset `names_all_years.csv` is included in this repository. If you need to regenerate it or access the original source:

1. Download from [Kaggle US Baby Names Dataset](https://www.kaggle.com/datasets/kaggle/us-baby-names)
2. Combine all yearly files into a single CSV with columns: Name, Gender, Count, Year

## Analysis Methodology

### Data Preprocessing
- Loaded and validated 2.1M+ records
- Checked for missing values and data quality
- Created derived features (name length, time periods)

### Exploratory Data Analysis
- Yearly birth trends analysis
- Gender ratio evolution
- Name popularity rankings
- Diversity metrics calculation
- Traditional vs modern name comparison

### Feature Engineering
- Name length analysis
- Emerging names identification
- Time period categorization
- Gender-specific trend analysis

### Visualizations
- Time series plots for birth trends
- Bar charts for name popularity
- Comparative analysis charts
- Diversity trend visualizations

## Key Insights

1. **Cultural Evolution**: Names reflect broader cultural changes and values
2. **Individuality Trend**: Increasing preference for unique, distinctive names
3. **Gender Patterns**: Different naming conventions for boys vs girls
4. **Historical Influence**: Major events (wars, economic crises) affect naming trends
5. **Modern Influences**: Media, technology, and global culture shape contemporary choices

## Data Limitations

- **Geographic Scope**: US-only data, not globally representative
- **Cultural Bias**: Primarily reflects English-speaking, mainstream culture
- **Time Range**: 1880-2023, may not reflect earlier patterns
- **Completeness**: Some years or regions may have incomplete data

## Ethical Considerations

- **Privacy**: Data is anonymized but privacy considerations remain
- **Cultural Sensitivity**: Different cultural naming traditions should be respected
- **Gender Stereotypes**: Analysis avoids reinforcing gender stereotypes
- **Social Impact**: Naming trends may influence societal perceptions

## Deliverables

1. **Public Communication**: [Blog Post](blog_post.md) - Engaging narrative for general audience
2. **GitHub Repository**: This repository with complete analysis code
3. **Presentation**: 8-minute presentation summarizing key findings

## Contributing

This project was completed as part of a data storytelling course. For questions or suggestions:

1. Open an issue in this repository
2. Contact the project authors
3. Fork the repository for your own analysis

## License

This project is for educational purposes. The dataset is publicly available and the analysis code is open source.

## Acknowledgments

- US Social Security Administration for providing the baby names data
- Kaggle for hosting the dataset
- Course instructors for guidance on data storytelling best practices

---

*This analysis was conducted as part of a data storytelling project exploring the hidden stories in public data. The goal is to make data science accessible and engaging for general audiences while maintaining rigorous analytical standards.*
