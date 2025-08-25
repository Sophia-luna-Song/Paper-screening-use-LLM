import pandas as pd

# Paths to your files
csv_path = 'F:\game\综述\综述框架\文章\综述版本的种子表型研究\seed.csv'  # Replace with your actual CSV file path
excel_path = 'F:\game\综述\综述框架\文章\综述版本的种子表型研究\c3v79-j3i5g.xlsx'  # Replace with your actual Excel file path
output_path = 'F:\\game\\综述\\综述框架\\文章\\综述版本的种子表型研究\\updated.xlsx'  # Desired output path

# Load the CSV and Excel files
csv_data = pd.read_csv(csv_path, encoding='ISO-8859-1')  # Specify encoding if needed
excel_data = pd.read_excel(excel_path)

# Create a dictionary from CSV with titles as keys and abstracts as values for fast lookup
abstract_dict = dict(zip(csv_data['Title'], csv_data['Abstract']))

# Add a new column for the matched abstracts in the Excel data
excel_data['Abstract'] = excel_data['Title'].map(abstract_dict)

# Save the updated Excel file
excel_data.to_excel(output_path, index=False, encoding='utf-8-sig')
print(f"Updated Excel file saved to: {output_path}")
