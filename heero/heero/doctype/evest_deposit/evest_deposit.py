# Import necessary libraries
import frappe
from frappe.model.document import Document
import requests
import hashlib
import json
import time

class EvestDeposit(Document):
    pass

# Function to create SHA-1 hash
def make_sha1(s, encoding="utf-8"):
    return hashlib.sha1(s.encode(encoding)).hexdigest()

# Function to create access key
def create_access_key(time):
    PARTNER_ID = "25974691"
    PARTNER_SECRET_KEY = "94e1979cbeee02d5fc820dfce9b155bf1a29dcb58a07d393899e144d7af93b10"
    TIME = time
    concatenated_string = PARTNER_ID + str(TIME) + PARTNER_SECRET_KEY
    ACCESS_KEY = make_sha1(concatenated_string)
    return ACCESS_KEY

# Function to get Evest token
def get_evest_token():
    url = "https://mena-evest.pandats-api.io/api/v3/authorization"
    l_time = int(time.time())
    access_key = create_access_key(l_time)
    partner_id = "25974691"
    data = {
        "partnerId": partner_id,
        "time": str(l_time),
        "accessKey": access_key,
    }
    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json",}
    r = requests.post(url, headers=headers, data=data_json)
    json_data = r.json()
    try:
        token = json_data["data"]["token"]
    except:
        token = None
    return token

# Function to fetch and update Evest deposits
def fetch_and_update_evest_deposits(page=1):
    token = get_evest_token()

    if token:
        while page:
            # Set your API endpoint URL
            api_url = f"https://mena-evest.pandats-api.io/api/v3/customers/deposits?page={page}"
            headers = {"Authorization": f"Bearer {token}"}

            # Make the GET request
            response = requests.get(api_url, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Process the response data
                deposits_data = response.json()["data"]

                # Update your records based on the fetched data
                for deposit in deposits_data:
                    # Create a new instance of your custom DocType
                    doc = frappe.new_doc("EvestDeposit")

                    # Set values for each field based on the fetched data
                    doc.customer_id = deposit.get("customerId")
                    doc.login = deposit.get("login")
                    doc.email = deposit.get("email")
                    doc.status= deposit.get("status")
					doc.ftd = deposit.get("ftd")
					doc.declinereason = deposit.get("DeclineReason")
					doc.created_time = deposit.get("Created Time")

                    # Save the document
                    doc.insert()

                # Check if there are more pages
                next_page = response.json().get("next")
                if next_page:
                    # Update the page for the next iteration
                    page = next_page
                else:
                    # If there is no next page, break out of the loop
                    break
            else:
                # Log an error or handle the failure appropriately
                print(f"Failed to fetch Evest deposits. Status Code: {response.status_code}")
                break
    else:
        print("Failed to obtain Evest token.")

# Run the function to fetch and update deposits (you can enqueue it as a background job)

