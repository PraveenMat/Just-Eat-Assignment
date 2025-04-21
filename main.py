import argparse  # For parsing CLI arguments
import requests  # HTTP requests to the Just Eat API
from tabulate import tabulate  # Pretty-printing tables in the console

# API endpoint template for fetching restaurant data by postcode
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
# User-Agent to avoid 403 responses
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)


def get_restaurants(postcode: str, limit: int = 10) -> list[dict]:
    """
    Fetches up to `limit` restaurants from the Just Eat API for a given UK postcode.

    Parameters:
    - postcode: UK postcode (spaces optional)
    - limit: maximum number of restaurants to return

    Returns:
    - List of restaurant objects (dictionaries)
    """
    # Remove spaces in postcode for URL
    safe_postcode = postcode.replace(" ", "")
    url = API_URL.format(postcode=safe_postcode)

    # Perform GET request with custom User-Agent header
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    # Raise an exception for HTTP errors (4xx/5xx)
    response.raise_for_status()

    # Parse JSON response
    data = response.json()
    # Extract the 'restaurants' list and limit to requested count
    return data.get("restaurants", [])[:limit]


def format_restaurant(index: int, restaurant: dict) -> list:
    """
    Formats a single restaurant record into a list suitable for tabular output.

    Parameters:
    - index: numeric position (for display)
    - restaurant: raw restaurant data from API

    Returns:
    - List: [index, name, cuisines, rating, address]
    """
    # Safely extract fields with fallbacks
    name = restaurant.get("name", "N/A")
    # Join multiple cuisines by comma, or fallback to N/A
    cuisines = ", ".join(c.get("name", "") for c in restaurant.get("cuisines", [])) or "N/A"
    # Extract star rating, if present
    rating = restaurant.get("rating", {}).get("starRating", "N/A")

    # Build full address string
    addr = restaurant.get("address", {})
    parts = [addr.get("firstLine", ""), addr.get("city", ""), addr.get("postalCode", "")]
    address = ", ".join(filter(None, parts)) or "N/A"

    return [index, name, cuisines, rating, address]


def print_restaurants(restaurants: list[dict]) -> None:
    """
    Prints a formatted table of restaurants to stdout.

    Parameters:
    - restaurants: List of restaurant dicts
    """
    # Prepare rows for tabulation
    rows = [format_restaurant(i + 1, r) for i, r in enumerate(restaurants)]
    headers = ["Index", "Name", "Cuisines", "Rating", "Address"]

    # Print table in 'pretty' format
    print(tabulate(rows, headers=headers, tablefmt="pretty"))


def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for postcode and limit.

    Returns:
    - argparse.Namespace with attributes 'postcode' and 'limit'
    """
    parser = argparse.ArgumentParser(
        description="List restaurants for a UK postcode."
    )
    parser.add_argument(
        "postcode",
        help="UK postcode, e.g. 'SW1A 1AA'"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max number of restaurants to display (default: 10)"
    )
    return parser.parse_args()


def main() -> None:
    """
    Main entry point: fetches and displays restaurant data.
    """
    # Parse CLI inputs
    args = parse_args()

    try:
        # Fetch restaurant data
        restaurants = get_restaurants(args.postcode, args.limit)
    except requests.RequestException as e:
        # Handle network/API errors
        print(f"Error fetching data: {e}")
        return

    # Display results or a 'no data' message
    if not restaurants:
        print("No restaurants found.")
    else:
        print_restaurants(restaurants)


if __name__ == "__main__":
    main()
