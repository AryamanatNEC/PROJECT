import argparse
from .google_spider import *
import csv
import json
def main():
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

    ads_data, shopping_results_data = get_shopping_data(formatted_query, use_proxy=use_proxy, custom_proxy=custom_proxy)
 
    '''
    with open("shopping_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link", "source", "price", "delivery", "extensions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ad in ads_data:
            writer.writerow(ad)
    '''        
        
    with open("shopping_results_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "link", "source", "price", "rating", "reviews", "delivery", "extensions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in shopping_results_data:
            writer.writerow(result)

    # Save to JSON
    #with open("shopping_data.json", "w", encoding="utf-8") as jsonfile:
    #    json.dump(ads_data, jsonfile, ensure_ascii=False, indent=2)

    with open("shopping_results_data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(shopping_results_data, jsonfile, ensure_ascii=False, indent=2)
   

if __name__ == "__main__":
    main() 