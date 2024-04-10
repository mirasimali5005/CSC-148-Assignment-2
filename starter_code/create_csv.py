import csv
import os

# Define the data for the CSV file
data = [
    ["Author", "Title", "Year", "Category", "Url", "Citations"],
    ["Author1", "paper1", "2023", "a:b:c", "http://example.com/doi1", "3"],
    ["Author1", "paper2", "2023", "a:b:c", "http://example.com/doi2", "5"],
    ["Author1", "paper3", "2023", "m:n", "http://example.com/doi3", "5"],
    ["Author1", "paper4", "2020", "m:o:p", "http://example.com/doi4", "1"],
    ["Author1", "paper5", "2022", "a:b:d:e", "http://example.com/doi5", "7"],
    ["Author1", "paper6", "2020", "a:f", "http://example.com/doi6", "2"],
]

# Get the current working directory
current_directory = os.getcwd()

# Specify the filename
file_path = os.path.join(current_directory, "sample_papers.csv")

# Write the data to a CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file created at {file_path}")
