import argparse
from .google_spider import *
from .next_page import *
from .append_pages import *
def main():
    csv_file = "shopping_results_data.csv"
    json_file = "shopping_results_data.json"
    try:
        # Empty CSV file
        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            csvfile.truncate(0)

        # Empty JSON file
        with open(json_file, "w", encoding="utf-8") as jsonfile:
            jsonfile.truncate(0)

        print("CSV and JSON files have been emptied.")

    except Exception as e:
        print("An error occurred:", e)
    parser = argparse.ArgumentParser(
        description="CLI Tool to scrape data from Google Shopping."
    )
    parser.add_argument(
        "query", type=str,
        help="The query of the product to be searched."
    )
    parser.add_argument(
        "--use-proxy", action="store_true",
        help="Use proxy for making requests.Syntax: google_spider [YOUR QUERY] --use-proxy"
    )
    parser.add_argument(
        "--custom-proxy", type=str,
        help="Custom proxy URL to use for requests.Syntax: google_spider [YOUR QUERY] --use-proxy --custom-proxy [YOUR.PROXY.URL:PORT]"
    )
    args = parser.parse_args()
    #search_query = get_user_input()
    search_query = args.query
    formatted_query = format_search_query(search_query) 
    custom_proxy = args.custom_proxy if args.custom_proxy else None
    use_proxy = args.use_proxy or bool(custom_proxy)

    get_shopping_data(formatted_query, use_proxy=use_proxy, custom_proxy=custom_proxy)
    next_page(formatted_query)
    append_shopping_data(use_proxy=use_proxy, custom_proxy=custom_proxy)
    
 

if __name__ == "__main__":
    main() 