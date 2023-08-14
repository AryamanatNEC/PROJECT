import os
import csv
import webbrowser

def open_links_from_file(index=1):
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        print(current_directory)
        csv_files = [f for f in os.listdir(current_directory) if f.endswith(".csv")]

        if  not csv_files:
            print("No CSV files found in the current directory.")
            return

        if index is None:
            print("Please specify an index to open a URL.")
            return

        all_links = []

        if csv_files:
            for csv_file in csv_files:
                with open(csv_file, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    links = [row["link"] for row in reader]
                    all_links.extend(links)

        if 0 <= index < len(all_links):
            link = all_links[index]
            if link:
                webbrowser.open_new_tab(link)
                print(f"Opened URL at index {index}: {link}")
            else:
                print(f"Empty link found at index {index}.")
        else:
            print("Invalid index.")

    except Exception as e:
        print("An error occurred:", e)
'''
# Example usage:
index_to_open = 3  # Replace with the desired index
open_links_from_file(index=index_to_open)
'''
