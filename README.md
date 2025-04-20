# Displaying Restaurant List

Using Just Eat API to display 10 results on the console using postcode. Details include the restaurant's name, cuisine, rating, and address. 

## How to Build, Compile and Run

1. **Requirements:**
   - Python 3.10 (Was coded and tested in this version of Python)
   - `requests` library (install using pip: `pip install requests`)
   - `tabulate ` library (install using pip: `pip install tabulate `)

2. **How to run the Script:**
   - Clone this repository to your machine and open up your preferred IDE.
   - Open the terminal and run this line:
     ```
     python main.py
     ```
3. **Issue Which Could be Faced Running the Script**
   - When the table gets printed, it might not be displayed correctly. Ensure that you have zoomed out so that the table is displayed correctly on the terminal. 

## Assumptions

**Note: Before implementing the solution, I used Postman to understand the structure of the API response and double check if authentication was needed.**
- Error handling is not necessary.
- Restaurants should have all the necessary data needed to display, but to have some error handling, I added messages (e.g. No Restaurant Name Found) to improve user experience where some restaurant data might be incomplete or missing.  
- There will be at least 10 restaurants displayed.

## Future Improvements

- Allow users to input a postcode and display the restaurant data rather than having a fixed postcode and add functionality to check if the postcode is valid.
- Have GUI to display the restaurant data.
- Add functionality to sort and filter the restaurant data based on rating or cuisine type. 
- Give the user the option to display more than 10 restaurants.

## Error Encountered
- **403 Error:**  
  When requesting the data from the API, I got a 403 error. From Googling, it was due to server rejecting the request due to not having a User-Agent header. Therefore, I added a User-Agent header to fix the issue.

  ***Reference: https://stackoverflow.com/questions/76997162/requests-in-python-returning-403***
  
