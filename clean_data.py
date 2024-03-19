import pandas as pd
import re

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
    df['price'] = round(df['price'] / exchange_rate, 2)
    print("Converting 'price' from Won to USD. Updated 'price' column:")
    print(df['price'].head())

def print_columns(df):
    print("Columns in the DataFrame:")
    print(df.columns)

def save_to_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to '{file_path}'.")

#return columns that contain korean characters
def check_korean_chars(df):
    korean_columns = []
    for column in df.columns:
        if df[column].apply(lambda x: bool(re.search('[^\x00-\x7F]+', str(x)))).any():
            korean_columns.append(column)
            print(f"Sample rows for column '{column}' with Korean characters:")
            print(df.loc[df[column].str.contains('[^\x00-\x7F]+', na=False), [column]].head())
    return korean_columns


def delete_korean_chars(df, columns):
    for column in columns:
        print(f"Deleting Korean characters in column '{column}'. Original values:")
        print(df[column].head())
        df[column] = df[column].str.replace('[^\x00-\x7F]+', '', regex=True)
    print("Deleting Korean characters. Updated DataFrame:")
    print(df)


def main():
    # Specify the file path
    folder = 'data/'
    file_path = 'wine_info.csv'
    korean_columns = []
    #Column to drop 
    columns_to_drop = ['local2', 'local3','local4', 'varieties2', 'varieties3', 'varieties4', 'varieties5', 'varieties6',
                    'varieties7', 'varieties8', 'varieties9', 'varieties10', 'varieties11', 'varieties12']


    
    # Load data
    df = load_data(folder + file_path)
    
    # Drop columns
    if df is not None:
        drop_columns(df, columns_to_drop)
    
    if df is not None:
        display_head(df)
        check_null(df)
        drop_null(df)
        if check_duplicates(df) > 0:
            print("Dropping duplicates...")
            drop_duplicates(df)
    
        convert_won_to_usd(df)
        korean_columns = check_korean_chars(df)
        delete_korean_chars(df, korean_columns)
        
        # Save cleaned data to a new file
        save_to_csv(df, 'clean_data/cleaned_wine_info.csv')

if __name__ == "__main__":
    main()
