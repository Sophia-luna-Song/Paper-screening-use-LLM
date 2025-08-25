import http.client
import json
import pandas as pd
import re
import traceback


def get_response_from_api(title, abstract):
    conn = http.client.HTTPSConnection("api.chatanywhere.tech")
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Based on the title and abstract:\n\n"
                           f"1. Determine if the phenotyping method is destructive or non-destructive: "
                           f"Label as 0 for destructive and 1 for non-destructive.\n\n"
                           f"2. Determine if the study is quantitative or qualitative phenotyping: "
                           f"Label as 0 for qualitative and 1 for quantitative.\n\n"
                           f"3. Assess the automation level of phenotyping: "
                           f"Label as 0 for fully manual, 1 for manual + equipment, and 3 for minimal human involvement.\n\n"
                           f"Reply in the format: Damage is n, Type is n, Automation is n !!!"
            }
        ]
    })
    headers = {
        'Authorization': 'Bearer sk-qPQtTU47NOASDBYmjpu6nPMad959c6ZbR53OkufCAfFjw7yJ',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def extract_labels(response_content):
    damage_match = re.search(r'Damage is (\d+)', response_content)
    type_match = re.search(r'Type is (\d+)', response_content)
    automation_match = re.search(r'Automation is (\d+)', response_content)

    damage = damage_match.group(1) if damage_match else None
    type_label = type_match.group(1) if type_match else None
    automation = automation_match.group(1) if automation_match else None

    return damage, type_label, automation


# Read the "Title" and "Abstract" columns from Excel file
excel_file_path = 'F:\game\综述\综述框架\文章\综述版本的种子表型研究\\updated.xlsx'
df = pd.read_excel(excel_file_path)

# Create an empty list to store results
results = []


# Define a function to save results
def save_results():
    results_df = pd.DataFrame(results, columns=["Title", "Damage", "Type", "Automation"])
    results_df.to_excel('F:\game\综述\综述框架\文章\综述版本的种子表型研究\分类后.xlsx', index=False,
                        encoding='utf-8-sig')
    print("Progress saved to '分类后.xlsx'")


# Iterate through each title and abstract
for index, row in df.iterrows():
    title = row["Title"]
    abstract = row.get("Abstract", "")  # Use empty string if abstract is not available

    try:
        response = get_response_from_api(title, abstract)

        # Debug output to view response content
        print("Response:", response)

        # Extract values
        damage, type_label, automation = extract_labels(response)

        results.append({
            "Title": title,
            "Damage": damage,
            "Type": type_label,
            "Automation": automation
        })
        print(f"Extracted for title '{title}': Damage={damage}, Type={type_label}, Automation={automation}")

    except Exception as e:
        # If an error occurs, print error message and save current results
        print(f"Error processing title '{title}': {e}")
        print(traceback.format_exc())
        save_results()
        break  # Stop the loop

# Final save of results
save_results()
print("Classification results saved to '去掉动物研究-后半部分.xlsx'")
