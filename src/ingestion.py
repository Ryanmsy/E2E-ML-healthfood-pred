import requests
import json
import time
from pathlib import Path

# --- CONSTANTS (The Hardwiring) ---
# These don't change often, so keeping them global is fine!
BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"
HEADERS = {"User-Agent": "MyHealthyFoodProject/1.0 (ryanmsy2601@gmail.com)"}

# --- THE FUNCTION ---
def ingestion(max_pages: int, destination_file: str): 
    # ^^^ We added destination_file here. 
    # Now the function asks: "How many pages?" AND "Where do I put them?"

    all_products = []
    
    print(f"Starting extraction for {max_pages} pages...")

    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        
        params = {
            "action": "process",
            "json": "1",
            "fields": "code,product_name,nutriments,nutrition_grades,categories_tags",
            "page_size": "100",
            "page": page
        }
        
        try:
            # We use the Global constants BASE_URL and HEADERS here. 
            # That is perfectly fine because they are constants.
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])

                if not products:
                    print("No more products found. Stopping.")
                    break
                    
                all_products.extend(products)
                print(f"  - Retrieved {len(products)} products.")
            else:
                print(f"  - Error: Status Code {response.status_code}")
                
        except Exception as e:
            print(f"  - Exception occurred: {e}")

        time.sleep(1.0) 

    # --- SAVING ---
    # We use the variable from '()' here.
    with open(destination_file, "w") as f:
        json.dump(all_products, f, indent = 4 )
    
    print(f'Successful. Saved to {destination_file}')

# --- EXECUTION ---

# Now you define the path outside, and pass it IN.
basepath = Path(__file__).resolve().parent
my_file_path = basepath.parent / "data" /   "raw_product_data.json"

# Run it!
ingestion(max_pages=30, destination_file=my_file_path)