# To requests is used to get the data
import requests
# Used to display the data in a table
from tabulate import tabulate

def main():
    # Used my home postcode
    url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/CR7 8JZ"
    
    # Added User-Agent header to fix the 403 issue
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    # Requesting the data 
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
    except Exception as e:
        print(f"Error fetching data: {e}")
        return
    
    data = response.json()
    # Returns restaurant data with key: "restaurants"
    restaurants = data.get('restaurants', [])
    
    # If no restaurants were found, then prints this message
    if not restaurants:
        print("No restaurants found.")
        return
    
    # List to hold the data for the table
    table_rows = []
    
    # Displaying the first 10 restaurants with the required fields
    for i, restaurant in enumerate(restaurants[:10], start=1):
        
        # Restaurant Name
        name = restaurant.get('name', 'No Restaurant Name Found')
        
        # Cuisine
        cuisines = restaurant.get('cuisines', [])
        # As there sometime multple cuisines, I join them to list out
        cuisines_names = ', '.join(c.get('name', 'Unknown Cuisine') for c in cuisines) if cuisines else 'Unknown Cuisine'
        
        # Rating
        rating = restaurant.get('rating', {}).get('starRating', 'No Rating Found')
        
        # Address
        addr = restaurant.get('address', {})
        first_line = addr.get('firstLine', '')
        city = addr.get('city', '')
        post_code = addr.get('postalCode', '')
        address = ', '.join([part for part in [first_line, city, post_code] if part])
        if not address:
            address = 'No Address Found'
        
        # Append the restaurant's data as a row
        table_rows.append([i, name, cuisines_names, rating, address])
    
    # Table headers
    headers = ["Index", "Name", "Cuisines", "Rating", "Address"]
    
    # Displays table
    print(tabulate(table_rows, headers=headers, tablefmt="pretty"))

if __name__ == '__main__':
    main()
