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
    # print(df.isnull())
    return df.isnull().sum()

def check_duplicates(df):
    print("Checking for duplicates:")
    print(df.duplicated().sum())
    return df.duplicated().sum()

def drop_duplicates(df):
    df.drop_duplicates(inplace=True)
    print("Dropping duplicates. Checking for duplicates after removal:")
    print(df.duplicated().sum())

def drop_null(df):
    df.dropna(inplace=True)
    print("Dropping rows with null values. Checking for null values after removal:")
    print(df.isnull().sum())

def drop_columns(df, columns):
    df.drop(columns=columns, inplace=True)
    print(f"Dropping columns: {columns}. Updated columns:")
    print(df.columns)
def convert_won_to_usd(df, exchange_rate=1315.57):
    print(df['price'].head())
    df['price'] /= exchange_rate
    print("Converting 'price' from Won to USD. Updated 'price' column:")
    print(df['price'].head())

def print_columns(df):
    print("Columns in the DataFrame:")
    print(df.columns)

def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to '{file_path}'.")

def main():
    # Specify the file path
    file_path = 'wine_info.csv'
    
    #Column to drop 
    columns_to_drop = ['varieties2', 'varieties3', 'varieties4', 'varieties5', 'varieties6',
                    'varieties7', 'varieties8', 'varieties9', 'varieties10', 'varieties11', 'varieties12']


    # Load data
    df = load_data(file_path)

    if df is not None:
        # Data exploration and cleaning
        print_columns(df)

        display_head(df)
        check_null(df)

        if check_duplicates(df) > 0:
            print("Dropping duplicates...")
            drop_duplicates(df)
    
        convert_won_to_usd(df)
        
        # Save cleaned data to a new file
        save_to_csv(df, 'cleaned_wine_info.csv')
if __name__ == "__main__":
    main()
