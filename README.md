# Professional Data Analyst - Mini Project 1
## Advanced Python Data Exploration & Automated Reporting

**Dataset:** `Sample - Superstore 2019.xls`  
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn

This project follows the requirements in the provided Mini Project 1 specification.

### Required tasks covered

- Import and inspect the dataset with Pandas.
- Clean missing values, duplicates, inconsistent text formats, and simple outliers.
- Use reusable preprocessing functions/methods.
- Create feature-engineered columns:
  - Profit Margin
  - Shipping Duration
  - Sales Performance Category
- Use modular functions and a simple Python class.
- Perform exploratory analysis.
- Perform correlation analysis.
- Analyze distributions and monthly trends.
- Create 8 visualizations.
- Generate KPI and analytical summaries automatically.
- Export cleaned data, summaries, correlation results, and charts.
- Reduce memory usage using simple Pandas numeric downcasting.
- Document the workflow in `Project_Workflow.ipynb`.

### Beginner-friendly implementation

Although the assignment is called **Advanced Mini-Project**, the implementation is intentionally kept understandable for a learner who has just studied the listed Python topics. The OOP requirement is met with one simple class, and the preprocessing is divided into clear methods instead of using complex frameworks or external pipelines.

### Files

- `main.py` - complete Python implementation.
- `Project_Workflow.ipynb` - documented notebook workflow.
- `Sample - Superstore 2019.xls` - required dataset.
- `cleaned_superstore.csv` - cleaned/exported dataset.
- `kpi_summary.csv` - KPI summary.
- `correlation_matrix.csv` - correlation analysis.
- `analytical_report.txt` - automated text report.
- `01_...png` through `08_...png` - eight visualizations.

### Run

Install:
`pip install pandas numpy matplotlib seaborn xlrd`

Then:
`python main.py`

The project reads the `Orders` sheet from the required Excel dataset.
