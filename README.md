# My Notepad

## Overview

My Notepad is a simple, command-line text editor built with Python. It allows users to create, open, edit, and save text documents. The application also integrates four independent microservices through REST APIs to provide additional functionality.

## Features

- **New:** Create a new text document.
- **Open:** Open an existing text file.
- **Edit:** Add or replace document contents.
- **Save:** Save changes to the current document.
- **Save As:** Save the document under a new filename.
- **Send Notification:** Send a notification through the notification microservice.
- **Convert Currency:** Convert an amount between currencies using the currency conversion microservice.
- **Calculate Days Remaining:** Calculate the number of days until a specified deadline.
- **Search Document:** Search document contents for lines containing a specified term.
- **Filter Document:** Find lines that exactly match the specified text.

## Requirements

- Python 3
- `requests` Python library
- All four microservices running locally

Install the required Python library:

```bash
pip install requests
```

## Running the Application

1. Start each of the four microservices in its respective terminal.
2. Ensure each service is listening on its configured port.
3. Run the Notepad application:

```bash
python notepad.py
```

The application will display a menu allowing users to select the desired operation.

## Microservice Communication

The application communicates with four independent microservices using HTTP POST requests and JSON data.

| Microservice | Endpoint | Port |
|---|---|---:|
| Deadline Calculator | `/calculate` | 5000 |
| Notification | `/send_notification` | 5001 |
| Currency Converter | `/convert` | 5002 |
| Search and Filter | `/search_filter` | 5003 |

### 1. Deadline Calculator

Calculates the number of days remaining until a specified date.

- **Request:** `deadline` (YYYY-MM-DD)
- **Response:** Deadline, days remaining, and status.

### 2. Notification Service

Sends a notification to a specified recipient.

- **Request:** `notification_type`, `recipient`, and `message`
- **Response:** Notification confirmation or error message.

### 3. Currency Converter

Converts a specified amount from one currency to another.

- **Request:** `amount`, `from_currency`, and `to_currency`
- **Response:** Original amount, converted amount, currencies, and exchange rate.

### 4. Search and Filter Service

Searches or filters document contents.

- **Request:** `records`, `query`, `search_fields`, and/or `filters`
- **Response:** Matching records and result count.

**Search:** Performs a partial text search. For example, searching for `milk` will match a line containing `I need to buy milk`.

**Filter:** Performs an exact field-value match. For example, filtering for `I need to buy milk` will only return a line matching that exact text.

## Error Handling

The application uses the Python `requests` library to communicate with its microservices.

- Connection errors are caught and displayed if a service is unavailable.
- HTTP response errors are handled by the application where applicable.
- Invalid currency amounts are caught and reported.
- The microservices return their respective error messages when a request cannot be processed.

## Notes

- Documents are stored as local text files.
- The application does not maintain a database.
- Microservices operate independently and must be started separately.
- Search and filter operations do not modify the original document contents.
- The application uses `127.0.0.1` / `localhost` for local microservice communication.
