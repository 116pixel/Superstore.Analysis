import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = "Sample - Superstore 2019.xls"



def clean_data(data):
    """Reusable preprocessing function."""
    data = data.copy()

    # Remove extra spaces from text values
    text_columns = data.select_dtypes(include="object").columns
    for column in text_columns:
        data[column] = data[column].astype(str).str.strip()

    # Convert dates and numeric columns
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    data["Ship Date"] = pd.to_datetime(data["Ship Date"], errors="coerce")
    data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
    data["Profit"] = pd.to_numeric(data["Profit"], errors="coerce")
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce")

    # Handle missing values
    for column in ["Sales", "Profit", "Quantity", "Discount"]:
        if data[column].isna().sum() > 0:
            data[column] = data[column].fillna(data[column].median())

    for column in ["Order Date", "Ship Date"]:
        if data[column].isna().sum() > 0:
            data[column] = data[column].fillna(method="ffill")

    # Remove duplicate records
    data = data.drop_duplicates()

    # Simple IQR outlier handling
    for column in ["Sales", "Profit"]:
        q1 = data[column].quantile(0.25)
        q3 = data[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        data[column] = data[column].clip(lower, upper)

    # Feature engineering
    data["Profit Margin"] = np.where(
        data["Sales"] != 0,
        data["Profit"] / data["Sales"],
        0
    )

    data["Shipping Duration"] = (
        data["Ship Date"] - data["Order Date"]
    ).dt.days

    average_sales = data["Sales"].mean()
    data["Sales Performance Category"] = np.where(
        data["Sales"] >= average_sales,
        "High",
        "Low"
    )

    data["Order Month"] = data["Order Date"].dt.to_period("M").astype(str)

    # Simple memory optimization
    data["Quantity"] = pd.to_numeric(data["Quantity"], downcast="integer")
    data["Discount"] = pd.to_numeric(data["Discount"], downcast="float")
    data["Sales"] = pd.to_numeric(data["Sales"], downcast="float")
    data["Profit"] = pd.to_numeric(data["Profit"], downcast="float")

    return data

class SuperstoreProject:
    """Simple class for the Superstore mini project."""

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = None

    def load_data(self):
        try:
            self.data = pd.read_excel(self.file_name, sheet_name="Orders")
            print("Data loaded successfully.")
            print("Rows and columns:", self.data.shape)
            return self.data
        except FileNotFoundError:
            print("Dataset file was not found.")
        except Exception as error:
            print("Could not read the Excel file.")
            print("Make sure the xlrd package is installed.")
            print("Error:", error)
        return None

    def inspect_data(self):
        print("\nFirst 5 rows:")
        print(self.data.head())

        print("\nData types:")
        print(self.data.dtypes)

        print("\nMissing values:")
        print(self.data.isna().sum())

        print("\nDuplicate rows:", self.data.duplicated().sum())

    def clean_data(self):
        """Call the reusable preprocessing function."""
        self.data = clean_data(self.data)
        return self.data

    def create_summary(self):
        data = self.data

        kpis = {
            "Total Sales": data["Sales"].sum(),
            "Total Profit": data["Profit"].sum(),
            "Average Sales": data["Sales"].mean(),
            "Average Profit": data["Profit"].mean(),
            "Total Orders": data["Order ID"].nunique(),
            "Average Shipping Duration": data["Shipping Duration"].mean()
        }

        kpi_table = pd.DataFrame(
            list(kpis.items()),
            columns=["Metric", "Value"]
        )

        sales_by_category = data.groupby("Category")["Sales"].sum()
        profit_by_region = data.groupby("Region")["Profit"].sum()
        monthly_sales = data.groupby("Order Month")["Sales"].sum()
        sales_by_segment = data.groupby("Segment")["Sales"].sum()

        return kpi_table, sales_by_category, profit_by_region, monthly_sales, sales_by_segment

    def correlation_analysis(self):
        numeric_data = self.data[[
            "Sales", "Quantity", "Discount", "Profit",
            "Profit Margin", "Shipping Duration"
        ]]
        correlation = numeric_data.corr()
        print("\nCorrelation Analysis:")
        print(correlation)
        correlation.to_csv("correlation_matrix.csv")
        return correlation

    def save_results(self, kpi_table):
        self.data.to_csv("cleaned_superstore.csv", index=False)
        kpi_table.to_csv("kpi_summary.csv", index=False)

        with open("analytical_report.txt", "w", encoding="utf-8") as file:
            file.write("Superstore Analytical Report\n")
            file.write("===========================\n")
            for _, row in kpi_table.iterrows():
                file.write(f'{row["Metric"]}: {row["Value"]:.2f}\n')

            file.write("\nThe report was generated automatically by the Python project.\n")

        print("\nResults exported successfully.")


def create_visualizations(data, sales_by_category, profit_by_region,
                          monthly_sales, sales_by_segment, correlation):
    sns.set_theme(style="whitegrid")

    # 1 Matplotlib - Sales by Category
    plt.figure(figsize=(8, 5))
    plt.bar(sales_by_category.index, sales_by_category.values)
    plt.title("Total Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("01_sales_by_category.png")
    plt.close()

    # 2 Matplotlib - Profit by Region
    plt.figure(figsize=(8, 5))
    plt.bar(profit_by_region.index, profit_by_region.values)
    plt.title("Total Profit by Region")
    plt.xlabel("Region")
    plt.ylabel("Profit")
    plt.tight_layout()
    plt.savefig("02_profit_by_region.png")
    plt.close()

    # 3 Seaborn - Monthly Sales Trend
    plt.figure(figsize=(11, 5))
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("03_monthly_sales_trend.png")
    plt.close()

    # 4 Matplotlib - Sales Share
    plt.figure(figsize=(7, 7))
    plt.pie(
        sales_by_category.values,
        labels=sales_by_category.index,
        autopct="%1.1f%%"
    )
    plt.title("Sales Share by Category")
    plt.tight_layout()
    plt.savefig("04_sales_share_by_category.png")
    plt.close()

    # 5 Seaborn - Sales vs Profit
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=data, x="Sales", y="Profit", hue="Category")
    plt.title("Sales vs Profit")
    plt.tight_layout()
    plt.savefig("05_sales_vs_profit.png")
    plt.close()

    # 6 Seaborn - Sales by Segment
    plt.figure(figsize=(8, 5))
    segment_plot = pd.DataFrame({
        "Segment": sales_by_segment.index,
        "Sales": sales_by_segment.values
    })
    sns.barplot(data=segment_plot, x="Segment", y="Sales", color="steelblue")
    plt.title("Sales by Customer Segment")
    plt.xlabel("Segment")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("06_sales_by_segment.png")
    plt.close()

    # 7 Seaborn - Profit Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(data=data, x="Profit", bins=30, kde=True, color="steelblue")
    plt.title("Profit Distribution")
    plt.tight_layout()
    plt.savefig("07_profit_distribution.png")
    plt.close()

    # 8 Seaborn - Correlation Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig("08_correlation_heatmap.png")
    plt.close()


def main():
    print("Superstore - Advanced Python Mini Project")

    project = SuperstoreProject(DATA_FILE)

    data = project.load_data()
    if data is None:
        return

    project.inspect_data()
    data = project.clean_data()

    kpi_table, sales_by_category, profit_by_region, monthly_sales, sales_by_segment = project.create_summary()
    correlation = project.correlation_analysis()

    create_visualizations(
        data,
        sales_by_category,
        profit_by_region,
        monthly_sales,
        sales_by_segment,
        correlation
    )

    project.save_results(kpi_table)

    print("\nKPI Summary:")
    print(kpi_table)
    print("\nProject completed successfully.")


if __name__ == "__main__":
    main()
