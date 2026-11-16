# Currently using two microservices via REST API
# Currency converter and notification service functional


import requests

current_file = None
text = ""


# -------------------------
# Notepad Functions
# -------------------------

def new_file():
    global current_file, text

    text = ""
    current_file = None

    current_file = input("Enter filename for new document: ")
    print("New document created.")


def open_file():
    global current_file, text

    current_file = input("Enter filename to open: ")

    with open(current_file, "r") as file:
        text = file.read()

    print("File opened successfully.")
    print(text)


def save_file():
    if current_file is None:
        save_as()
        return

    with open(current_file, "w") as file:
        file.write(text)

    print("File saved successfully.")


def save_as():
    global current_file

    current_file = input("Enter filename: ")
    save_file()


def edit_text():
    global text

    print("Enter your text (type SAVE on a new line to finish):")

    lines = []

    while True:
        line = input()

        if line == "SAVE":
            break

        lines.append(line)

    text = "\n".join(lines)


# -------------------------
# Search and Filter API
# -------------------------


SEARCH_URL = "http://127.0.0.1:5003/search_filter"


def call_search_service(records, query="", search_fields=None, filters=None):

    data = {
        "records": records,
        "query": query,
        "filters": filters or {}
    }

    if search_fields is not None:
        data["search_fields"] = search_fields

    response = requests.post(
        SEARCH_URL,
        json=data,
        timeout=5
    )

    response.raise_for_status()

    return response.json()["results"]

def search_document():

    if not text:
        print("There is no document text to search.")
        return

    records = [{"text": line} for line in text.splitlines()]

    query = input("Enter search term: ")

    try:
        results = call_search_service(
            records,
            query=query,
            search_fields=["text"]
        )

        print(f"\nFound {len(results)} matching lines:")

        for result in results:
            print(result["text"])

    except requests.exceptions.RequestException as error:
        print("Unable to connect to search service.")
        print(error)

def filter_document():

    if not text:
        print("There is no document text to filter.")
        return

    records = [{"text": line} for line in text.splitlines()]

    query = input("Enter the exact text of the line to find: ")

    try:
        results = call_search_service(
            records,
            filters={"text": query}
        )

        print(f"\nFound {len(results)} matching lines:")

        for result in results:
            print(result["text"])

    except requests.exceptions.RequestException as error:
        print("Unable to connect to search service.")
        print(error)


# -------------------------
# Notification API
# -------------------------

def api_request_notification():

    notification_type = input("Enter notification type: ")
    recipient = input("Enter recipient: ")
    message = input("Enter message: ")

    data = {
        "notification_type": notification_type,
        "recipient": recipient,
        "message": message
    }

    try:
        response = requests.post(
            "http://localhost:5001/send_notification",
            json=data,
            timeout=5
        )

        api_response(response)

    except requests.exceptions.RequestException as error:
        print("Unable to connect to notification service.")
        print(error)


def api_response(response):

    result = response.json()

    if response.status_code == 200:
        print("\nNotification sent successfully!")
        print(result["notification"])

    else:
        print("\nNotification error:")
        print(result["message"])


# -------------------------
# Currency API
# -------------------------

def currency_request():

    amount = float(input("Enter amount: "))
    from_currency = input("Convert from: ").upper()
    to_currency = input("Convert to: ").upper()

    data = {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency
    }

    try:
        response = requests.post(
            "http://localhost:5002/convert",
            json=data,
            timeout=5
        )

        currency_response(response)

    except requests.exceptions.RequestException as error:
        print("Unable to connect to currency service.")
        print(error)

    except ValueError:
        print("Please enter a valid amount.")


def currency_response(response):

    result = response.json()

    if response.status_code == 200:
        print("\nCurrency conversion successful!")
        print(
            f'{result["original_amount"]} '
            f'{result["from_currency"]} = '
            f'{result["converted_amount"]} '
            f'{result["to_currency"]}'
        )

    else:
        print("\nCurrency conversion error:")
        print(result["message"])

# -------------------------
# Deadline API
# -------------------------

def deadline_request():

    deadline = input("Enter deadline (YYYY-MM-DD): ")

    data = {
        "deadline": deadline
    }

    try:
        response = requests.post(
            "http://localhost:5000/calculate",
            json=data,
            timeout=5
        )

        deadline_response(response)

    except requests.exceptions.RequestException as error:
        print("Unable to connect to deadline service.")
        print(error)


def deadline_response(response):

    result = response.json()

    if response.status_code == 200:
        print("\nDeadline calculation successful!")
        print(f'Deadline: {result["deadline"]}')
        print(f'Days remaining: {result["days_remaining"]}')
        print(f'Status: {result["status"]}')

    else:
        print("\nDeadline calculation error:")
        print(result["error"])


# -------------------------
# Main Application
# -------------------------

def main():
    while True:
        print("\n--- My Notepad ---")
        print("1. New")
        print("2. Open")
        print("3. Edit")
        print("4. Save")
        print("5. Save As")
        print("6. Send Notification")
        print("7. Convert Currency")
        print("8. Calculate Days Remaining")
        print("9. Search Document")
        print("10. Filter Document")
        print("11. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            new_file()
        elif choice == "2":
            open_file()
        elif choice == "3":
            edit_text()
        elif choice == "4":
            save_file()
        elif choice == "5":
            save_as()
        elif choice == "6":
            api_request_notification()
        elif choice == "7":
            currency_request()
        elif choice == "8":
            deadline_request()
        elif choice == "9":
            search_document()
        elif choice == "10":
            filter_document()
        elif choice == "11":  
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
