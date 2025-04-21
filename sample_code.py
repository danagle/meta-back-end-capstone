import requests

BASE_URL = "http://localhost:8000"


def create_user_if_not_exists(username, password, email):
    """
    Creates a new user via the API if the username does not already exist.

    Parameters:
        username (str): The desired username for the new user.
        password (str): The password for the new user.
        email (str): The email address for the new user.

    Behavior:
        - Sends a POST request to the API endpoint `/auth/users/`.
        - If the user is created successfully (HTTP 201), prints a success message.
        - If the user already exists (HTTP 400), prints a warning.
        - If another error occurs, prints the error details.

    Returns:
        None

    Example:
        create_user_if_not_exists("johndoe", "securepassword", "john@example.com")
    """
    user_data = {
        "username": username,
        "password": password,
        "email": email
    }

    response = requests.post(f"{BASE_URL}/auth/users/", json=user_data)

    if response.status_code == 201:
        print(f"✅ User '{username}' created successfully.")
    elif response.status_code == 400:
        errors = response.json()
        if 'username' in errors and 'already exists' in str(errors['username']):
            print(f"⚠️ User '{username}' already exists.")
        else:
            print(f"❌ User creation failed: {errors}")
    else:
        print(f"❌ Unexpected error: {response.status_code} - {response.text}")


def authenticate_user(username, password):
    """
    Authenticates a user and retrieves an authentication token from the API.

    Parameters:
        username (str): The user's username.
        password (str): The user's password.

    Returns:
        str or None: The authentication token if login is successful; otherwise, None.

    Behavior:
        - Sends a POST request to the `/auth/token/login/` endpoint.
        - If credentials are valid (HTTP 200), returns the token and prints a success message.
        - If authentication fails, prints an error message with status and response content.

    Example:
        token = authenticate_user("johndoe", "securepassword")
        if token:
            print("Token:", token)
    """
    auth_data = {
        "username": username,
        "password": password
    }

    auth_response = requests.post(f"{BASE_URL}/auth/token/login/", data=auth_data)

    if auth_response.status_code == 200:
        token = auth_response.json().get("auth_token")
        print("✅ Authentication successful.")
        return token
    else:
        print("❌ Authentication failed:", auth_response.status_code, auth_response.text)
        return None


def get_current_user(auth_token):
    """
    Retrieves and returns the username of the currently authenticated user.

    Parameters:
        auth_token (str): The authentication token for the API.

    Returns:
        str or None: The username of the authenticated user if the request is successful;
                     otherwise returns None.

    Side Effects:
        Prints a success message with the username if authentication succeeds,
        or an error message with the status code and response text if it fails.

    Example:
        user = get_current_user("your_auth_token")
    """
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json"
    }

    auth_response = requests.get(f"{BASE_URL}/auth/users/me/", headers=headers)

    if auth_response.status_code == 200:
        username = auth_response.json().get("username")
        print(f"✅ Authenticated user: {username}")
        return username
    else:
        print("❌ Authentication failed:", auth_response.status_code, auth_response.text)
        return None


def create_menu_items(auth_token, menu_items_list):
    """
    Creates multiple menu items by sending POST requests to the API.

    Parameters:
        auth_token (str): The authentication token for the API.
        menu_items_list (list): A list of dictionaries, each representing a menu item with 
                                keys 'title', 'price', and 'inventory'.

    Example:
        menu_items = [
            {"title": "Burger", "price": "8.99", "inventory": 20},
            {"title": "Pasta", "price": "12.50", "inventory": 15}
        ]
        create_menu_items("your_token_here", menu_items)

    Outputs:
        Prints a success or failure message for each item created.
    """
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json"
    }

    for item in menu_items_list:
        response = requests.post(f"{BASE_URL}/restaurant/menu/", json=item, headers=headers)
        if response.status_code == 201:
            print(f"✅ Created '{item['title']}' menu item.")
        else:
            print(f"❌ Failed to create '{item['title']}': {response.status_code} - {response.text}")


def count_menu_items(auth_token):
    """
    Counts the number of menu items available on the restaurant menu.

    Parameters:
        auth_token (str): The authentication token for the API.

    Returns:
        int: The number of menu items if the request is successful; 
             otherwise, returns -1 to indicate failure.

    Behavior:
        - Sends a GET request to the `/restaurant/menu/` endpoint with the provided authorization token.
        - If successful (HTTP 200), prints and returns the count of menu items.
        - If the request fails, prints an error message with status and response details, and returns -1.

    Example:
        item_count = count_menu_items("your_auth_token_here")
        if item_count != -1:
            print(f"Menu has {item_count} items.")
    """
    headers = {
        "Authorization": f"Token {auth_token}"
    }

    response = requests.get(f"{BASE_URL}/restaurant/menu/", headers=headers)

    if response.status_code == 200:
        menu_items = response.json()
        print(f"✅ There are {len(menu_items)} items on the restaurant menu.")
        return len(menu_items)
    else:
        print(f"❌ Failed to fetch menu items: {response.status_code} - {response.text}")
        return -1


def add_a_table_booking(auth_token):
    """
    Adds a table booking for a specified restaurant using the API.

    Parameters:
        auth_token (str): The authentication token for the API.

    Returns:
        None: Prints success or failure message based on the result of the POST request.

    Behavior:
        - Sends a POST request to the `/restaurant/booking/tables/` endpoint with the booking data.
        - If the request is successful (HTTP 201), prints the created booking details.
        - If the request fails, prints an error message with the status code and response content.

    Example:
        add_a_table_booking("your_auth_token_here")
    """
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json"
    }

    booking_data = {
        "name": "John Doe",
        "no_of_guests": 4,
        "booking_date": "2025-04-20T18:30:00Z"  # Use ISO 8601 format
    }

    response = requests.post(f"{BASE_URL}/restaurant/booking/tables/", json=booking_data, headers=headers)

    if response.status_code == 201:
        print("✅ Table booking added:", response.json())
    else:
        print(f"❌ Failed to create table booking: {response.status_code}")
        print(response.text)


def list_bookings(auth_token):
    """
    Fetches and prints all table bookings from the restaurant's booking API.

    Parameters:
        auth_token (str): The authentication token for the API.

    Returns:
        list or None: A list of booking dictionaries if the request is successful;
                      otherwise, returns None.

    Behavior:
        - Sends a GET request to the `/restaurant/booking/tables/` endpoint with the provided authorization token.
        - If the request is successful (HTTP 200), prints the list of bookings with details like name and number of guests.
        - If the request fails, prints an error message with status code and response content.

    Example:
        bookings = list_bookings("your_auth_token_here")
        if bookings:
            print(f"Total bookings: {len(bookings)}")
    """
    headers = {
        "Authorization": f"Token {auth_token}"
    }

    response = requests.get(f"{BASE_URL}/restaurant/booking/tables/", headers=headers)

    if response.status_code == 200:
        bookings = response.json()
        print(f"✅ Found {len(bookings)} bookings:")
        for booking in bookings:
            print(f" - {booking['name']} ({booking['no_of_guests']} guests)")
        return bookings
    else:
        print(f"❌ Failed to fetch bookings: {response.status_code} - {response.text}")
        return None


if __name__ == "__main__":

    user_details = {
        "username": "script_user",
        "password": "script_pass123",
        "email": "script_user@domain.local"
    }

    create_user_if_not_exists(**user_details)

    auth_token = authenticate_user(user_details["username"], user_details["password"])

    get_current_user(auth_token)

    items_count = count_menu_items(auth_token)

    if items_count == 0:
        menu_items = [
            {"title": "Spaghetti", "price": "10.50", "inventory": 20},
            {"title": "Cheeseburger", "price": "8.99", "inventory": 15},
            {"title": "Caesar Salad", "price": "7.25", "inventory": 10},
            {"title": "Grilled Salmon", "price": "14.75", "inventory": 8},
            {"title": "Chicken Tacos", "price": "9.50", "inventory": 12},
        ]
        create_menu_items(auth_token, menu_items)
        items_count = count_menu_items(auth_token)

    add_a_table_booking(auth_token)
    list_bookings(auth_token)
