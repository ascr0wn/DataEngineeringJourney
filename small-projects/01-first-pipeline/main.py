#run this file from location: /home/ascr0wn/DataEngineeringJourney/small-projects/01-first-pipeline
import sys
import pandas as pd

def main():
    print("Name of this script:", sys.argv[0])
    #These lines are for when we input the file path as a command line argument using sys arguments. For now, we will use a hardcoded file path to read the CSV file.
    #filePath = sys.argv[1] # Get the file path from the command line argument
    #my_data = pd.read_csv(filePath)
    df = pd.read_csv('./sampleData1.csv')
    print("\n\n", "Sample Data from the CSV file before cleaning:\n", df, "\n\n")

    # Data Cleaning Stars Here
    df['age'] = df['age'].fillna(df['age'].mean()) # Fill NaN values in the 'age' column with the mean of the 'age' column
    df['age'] = df['age'].astype(int) # Convert the 'age' column to integer type

    df['city'] = df['city'].replace('na', 'Unknown') # Replace 'na' values in the 'city' column with 'Unknown'
    df['city'] = df['city'].str.title()

    df['salary'] = pd.to_numeric(df['salary'], errors='coerce')# Convert the 'salary' column to numeric, setting errors to NaN
    df['salary'] = df['salary'].fillna(df['salary'].median()) # Fill NaN values in the 'salary' column with the median of the 'salary' column
    df['salary'] = df['salary'].astype(int) # Convert the 'salary' column to int type

    print("Sample Data from the CSV file after cleaning:\n", df)

if __name__ == "__main__":
    main()
