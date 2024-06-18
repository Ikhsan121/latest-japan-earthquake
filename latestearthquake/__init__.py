from time import sleep
from matplotlib import pyplot as plt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def data_extraction():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.data.jma.go.jp/multi/quake/index.html?lang=en")
    sleep(2)
    table = driver.find_element(By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    # empty data list
    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        temp = []
        for col in cols:
            temp.append(col.text)
        data.append(temp)
    driver.close()
    return data

def show_data():
    # Define column names
    columns = ['Observed at', 'Place name of epicenter', 'Magnitude', 'Maximum seismic intensity',
               'Date and time of issuance']

    # Create DataFrame
    df = pd.DataFrame(data_extraction(), columns=columns)
    # Remove the first row
    df = df.drop(index=0)

    # Reset the index after dropping the row
    df = df.reset_index(drop=True)
    # Print the DataFrame
    plt.figure(figsize=(12, 6))
    df['Magnitude'] = pd.to_numeric(df['Magnitude'])
    # Plotting based on row index and a specific column (e.g., 'Column3')
    df['Magnitude'].plot(kind='line', marker='o')

    # Adding labels and title
    plt.xlabel('Event')
    plt.ylabel('Magnitude')
    plt.title('Plot of Magnitude vs Event')
    plt.gca().invert_xaxis()
    # Show plot
    plt.show()

def create_csv():
    # Define column names
    columns = ['Observed at', 'Place name of epicenter', 'Magnitude', 'Maximum seismic intensity',
               'Date and time of issuance']

    # Create DataFrame
    df = pd.DataFrame(data_extraction(), columns=columns)
    # Remove the first row
    df = df.drop(index=0)

    # Reset the index after dropping the row
    df = df.reset_index(drop=True)

    # set numerical data type for column Magnitude
    df['Magnitude'] = pd.to_numeric(df['Magnitude'])

    # Specify the file path where you want to save the CSV file
    csv_file_path = 'earthquake-data.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

    print(f"CSV file saved successfully to '{csv_file_path}'")

