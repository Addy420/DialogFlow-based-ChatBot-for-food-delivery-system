import re

# Function to generate a string representation from a food dictionary
def get_str_from_food_dict(food_dict: dict):
    # Generate a string of food items with their respective quantities
    result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
    return result

# Function to extract session ID from a given session string
def extract_session_id(session_str: str):
    # Using regular expression to extract session ID from the session string
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        # If a match is found, return the extracted session ID
        extracted_string = match.group(1)
        return extracted_string

    # If no match is found, return an empty string
    return ""

