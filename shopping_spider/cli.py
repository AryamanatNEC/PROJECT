import argparse
from .google_spider import *
from .next_page import *
from .append_pages import *
#from .site_opener import *
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
        help="Custom proxy URL to use for requests.Syntax: google_spider [YOUR QUERY] --custom-proxy [YOUR.PROXY.URL:PORT]"
    )
    '''
    parser.add_argument(
        "--open_site", type=int,
        help="Open URL Link."
    )
    '''
    args = parser.parse_args()
    #search_query = get_user_input()
    search_query = args.query
    formatted_query = format_search_query(search_query) 
    use_proxy = args.use_proxy 
    custom_proxy = args.custom_proxy if args.custom_proxy else None

    get_shopping_data(formatted_query, use_proxy=use_proxy,custom_proxy=custom_proxy)  # Pass custom_proxy argument
    next_page(formatted_query, use_proxy=use_proxy,custom_proxy=custom_proxy)  # Pass custom_proxy argument
    append_shopping_data(use_proxy=use_proxy,custom_proxy=custom_proxy)  # Pass custom_proxy argument
    '''
    if args.open_site:
        index=args.open_site
        open_links_from_file(index)
        '''
    
 

if __name__ == "__main__":
    main() 