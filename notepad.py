
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
# Notification API
# -------------------------

def api_request():

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
    from_currency = input("Convert from (USD/EUR/GBP/CAD): ").upper()
    to_currency = input("Convert to (USD/EUR/GBP/CAD): ").upper()

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
        print("8. Exit")

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
            api_request()
        elif choice == "7":
            currency_request()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
