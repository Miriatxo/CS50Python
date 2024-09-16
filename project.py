import json
import requests
import re
from datetime import datetime
import dateutil.parser
from deep_translator import GoogleTranslator


# Donostia city cultural events search engine. Prompts the user for search criteria: 1 compulsory (event category)
# and 2 optional (date and keyword), and prints formatted search results on the terminal
def main():
    result = query()
    if result:
        filtered = filter(result)
        if filtered:
            translated = translate(filtered)
            print_cards(translated)
        else:
            print("No results found.")
    else:
        print("No results found.")


# Prompts the user for an event type until they enter a valid type
def get_type():
    types = {"1": "music", "2": "art", "3": "theater", "4": "dance", "5": "cinema", "6": "children",
              "one": "music", "two": "art", "three": "theater", "four": "dance", "five": "cinema", "six": "children"}

    pattern1 = r"^[1-7]|[1-7]\.|(one|two|three|four|five|six|seven)$"
    pattern2 = r"^music|art|theater|dance|cinema|children|course$"
    pattern3 = r"^([1-7]|[1-7]\.|(one|two|three|four|five|six|seven))\s?(music|art|theater|dance|cinema|children|course)$"

    while True:
        type_input = input("Select an event category to see all upcoming events:\n1. Music\n2. Art\n3. Theater\n4. Dance\n5. Cinema\n6. Children\n7. Course\n").lower().strip()

        match1 = re.search(pattern1, type_input)
        match2 = re.search(pattern2, type_input)
        match3 = re.search(pattern3, type_input)

        if match1:
            type = types[match1.group()]
            break
        elif match2:
            type = match2.group()
            break
        elif match3:
            type = match3.group(3)
            break

        print("Please choose 1 (music), 2 (art), 3 (theater), 4 (dance), 5 (cinema), 6 (children), or 7 (course) to proceed with your search.")

    return type


# Prompts user for optional date and, if date is provided, validates input
# and returns date converted into API-friendly format (otherwise returns None)
def get_date():
    while True:
            user_input = input("Enter date (optional): ").lower().strip()
            if not user_input:
                return None
            try:
                date = dateutil.parser.parse(user_input, dayfirst=False)
                formatted_date = date.strftime('%Y-%m-%d')
                return formatted_date
            except ValueError:
                print("Invalid date format. Please use format: march 4, 03/04, etc., or hit Enter to skip entering date.")


# Prompts user for optional keyword and returns keyword, or None (if user doesn't enter keyword)
def get_keyword():
    keyword = input("Enter keyword (optional): ").lower().strip()
    return keyword if keyword else None


# Queries Open Data Euskadi API
def query():
    # Translate user given type into corresponding API type
    type_mapping = {
        "music": "1",
        "art": "3",
        "theater": "2",
        "dance": "4",
        "cinema": "9",
        "children": "14",
        "course": "11"
    }

    # Get type, a required search criterion, and translate into API-given number
    type = get_type()
    type_code = type_mapping[type]

    # Get date, an optional search criterion
    date = get_date()

    # Construct the URL based on whether the date is provided
    base_url = "https://api.euskadi.eus/culture/events/v1.0/events"

    if date:
        year, month, day = date.split("-")
        url = f"{base_url}/byType/{type_code}/byDate/{year}/{month}/{day}"
    else:
        url = f"{base_url}/byType/{type_code}"

    # Perform the GET request
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return None

    # Access the 'items' list of dictionaries from the response data
    events = data.get('items', [])

    return events


def filter(data):
    # Ensure data is a list
    if not isinstance(data, list):
        raise TypeError("Data should be a list of events")

    # Get keyword to filter results (if not None)
    keyword = get_keyword()

    # Create list excluding irrelevant events
    filtered_data = []

    for event in data:
        if isinstance(event, dict):  # Ensure event is a dictionary
            # Exclude events outside of Donostia or in Basque
            if event.get("municipalityEu") == "Donostia-San Sebastián" and event.get("language") != "EU":
                # Exclude events that take longer than three months
                start_date = event.get("startDate")
                end_date = event.get("endDate")
                start_date = dateutil.parser.parse(start_date, dayfirst=False)
                end_date = dateutil.parser.parse(end_date, dayfirst=False)
                duration = end_date - start_date
                if duration.days < 90:
                    # If keyword was given, add event to filtered_data only if some relevant value includes keyword
                    if keyword:
                        if (keyword in event.get("descriptionEs", "").lower() or keyword in event.get("descriptionEu", "").lower()
                        or keyword in event.get("placeEs", "").lower() or keyword in event.get("placeEu", "").lower()
                        or keyword in event.get("typeEs", "").lower() or keyword in event.get("typeEu", "").lower()
                        or keyword in event.get("nameEs", "").lower() or keyword in event.get("nameEu", "").lower()
                        or keyword in event.get("establishmentEs", "").lower() or keyword in event.get("establishmentEu", "").lower()
                        ):
                            filtered_data.append(event)
                    # If no keyword was given, add event to filtered_data
                    else:
                        filtered_data.append(event)

    # If keyword was provided and no matching events were found, inform the user
    if keyword and not filtered_data:
        print("No matches found with keyword provided.")

    return filtered_data


# Takes dictionary list in Spanish and Basque and
# outputs English translation of interesting content
def translate(data):
    if not data:
        return data  # Return original list if it's empty or None

    translated_events = []

    for event in data:
        translated_event = {}
        for key, value in event.items():
            try:
                if key == "nameEs" and value:
                    translation = GoogleTranslator(source="es", target="en").translate(value)
                    translated_event.update({"Name": translation})
                if key == "startDate" and value:
                    # Reformat date
                    date_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                    translated_event.update({"Date": formatted_date})
                if key == "openingHoursEs" and value:
                    translation = GoogleTranslator(source="es", target="en").translate(value)
                    translated_event.update({"Opening Hours": translation})
                if key == "establishmentEs" and value:
                    translation = GoogleTranslator(source="es", target="en").translate(value)
                    translated_event.update({"Establishment": translation})
                if key == "sourceUrlEs" and value:
                    translated_event.update({"Event Website": value})  # No need to translate URLs
                if key == "priceEs" and value:
                    translation = GoogleTranslator(source="es", target="en").translate(value)
                    translated_event.update({"Price": translation})
                if key == "purchaseUrlEs" and value:
                    translated_event.update({"Purchase Here": value})  # No need to translate URLs
                if key == "descriptionEs" and value:
                    translation = GoogleTranslator(source="es", target="en").translate(value)
                    translated_event.update({"Description": clean_html(translation)})
            except Exception as e:
                print(f"Error translating {key}: {e}")
                continue

        translated_events.append(translated_event)

    return translated_events


# Removes HTML tags from a string
def clean_html(raw_html):
    # Use a regex to remove HTML tags
    clean_text = re.sub(r"<.*?>|\r|\n", "", raw_html)
    # Collapse multiple spaces into a single space
    clean_text = re.sub(r'\s+', ' ', clean_text)
    # Trim leading/trailing spaces
    return clean_text.strip()


# Takes list of dictionaries and prints them in table-like format
def print_cards(data):
    if not data:
        print("No data to display.")
        return

    card_template = """

    -----------------------------------------

    Name: {Name}

    Date: {Date}

    Opening Hours: {Opening_Hours}

    Establishment: {Establishment}

    Event Website: {Event_Website}

    Price: {Price}

    Purchase Here: {Purchase_Website}

    Description: {Description}

    -----------------------------------------
    """
    for event in data:
        print(card_template.format(
            Name=event.get("Name", "N/A"),
            Date=event.get("Date", "N/A"),
            Opening_Hours=event.get("Opening Hours", "N/A"),
            Establishment=event.get("Establishment", "N/A"),
            Event_Website=event.get("Event Website", "N/A"),
            Price=event.get("Price", "N/A"),
            Purchase_Website=event.get("Purchase Here", "N/A"),
            Description=event.get("Description", "N/A")
        ))



if __name__ == "__main__":
    main()




