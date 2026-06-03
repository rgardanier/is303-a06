'''
Ryan Gardanier
IS 303
Retail Analysis

Inputs:
- retail_sales.csv: columns: date, store, product, category, quantity, unit_price

processes:
load_data(): reads the CSV file and loads it into a DataFrame.
clean_data(): handles missing values, removes duplicates, changes everthing to title case, and converts data types as necessary.
analyze_data(): performs analysis such as total sales by category, average sales per product, and identifies top-selling products.
visualize_data(): creates visualizations like bar charts for sales by category


Outputs:
- Summary statistics of sales by category and product.
- printed table to total sales by category
- top 5 selling products printed table
- Visualizations of sales trends saved as sales_by_category.png 

'''
import pandas as pd
import matplotlib.pyplot as plt


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def clean_data(df):
    # Handle missing values
    df = df.dropna()
    # Remove duplicates
    df = df.drop_duplicates()
    # Change to title case
    df['product'] = df['product'].str.title()
    df['category'] = df['category'].str.title()
    df['store'] = df['store'].str.title()
    # Convert data types
    df['unit_price'] = df['unit_price'].astype(str).str.replace('$', '', regex=False).astype(float)
    df['date'] = pd.to_datetime(df['date'])
    return df


def validate_data(df):
    # Check for missing values
    assert df['unit_price'].notna().all(), "Missing Values in unit_price"
    assert (df['unit_price'] > 0).all(), "unit_price should be positive"
    assert df['quantity'].notna().all(), "Missing Values in quantity"
    assert (df['quantity'] > 0).all(), "quantity should be positive"
    print("Data validation passed.")


def analyze_data(df):
    # add revenue column
    df['revenue'] = df['unit_price'] * df['quantity']
    # Total sales by category
    sales_by_category = df.groupby('category')['revenue'].sum()
    top_selling_products = df.groupby('product')['revenue'].sum().sort_values(ascending=False).head(5)
    print("\n ==== Total Sales by Category ====")
    print(sales_by_category)
    print("\n ==== Top 5 Selling Products ====")
    print(top_selling_products)
    return df, sales_by_category


def visualize_data(sales_by_category):
    sales_by_category.plot(kind='bar', color='skyblue')
    plt.title('Total Sales by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sales_by_category.png')
    plt.show()


def main():
    # Load data
    df = load_data('retail_sales.csv')
    # Clean data
    cleaned_df = clean_data(df)
    # validate cleaned data
    validate_data(cleaned_df)
    # Analyze data
    new_df, sales_by_category = analyze_data(cleaned_df)
    # Visualize data
    visualize_data(sales_by_category)


if __name__ == '__main__':
    main()