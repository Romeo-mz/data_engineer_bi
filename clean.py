import pandas as pd

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{file_path}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Unable to parse data from '{file_path}'. Please check the file format.")
        return None

def display_head(df):
    print("Showing the first few rows of the DataFrame:")
    print(df.head())

def check_null(df):
    print("Checking for null values:")
    print(df.isnull().sum())

def check_duplicates(df):
    print("Checking for duplicates:")
    print(df.duplicated().sum())

def drop_duplicates(df):
    df.drop_duplicates(inplace=True)
    print("Dropping duplicates. Checking for duplicates after removal:")
    print(df.duplicated().sum())

def drop_null(df):
    df.dropna(inplace=True)
    print("Dropping rows with null values. Checking for null values after removal:")
    print(df.isnull().sum())

def convert_won_to_usd(df, exchange_rate=1315.57):
    df['price'] /= exchange_rate
    print("Converting 'price' from Won to USD. Updated 'price' column:")
    print(df['price'].head())

def main():
    # Specify the file path
    file_path = 'wine_info.csv'
    
    # Load data
    df = load_data(file_path)

    if df is not None:
        # Data exploration and cleaning
        display_head(df)
        check_null(df)
        check_duplicates(df)
        drop_duplicates(df)
        check_duplicates(df)
        drop_null(df)
        convert_won_to_usd(df)

if __name__ == "__main__":
    main()
