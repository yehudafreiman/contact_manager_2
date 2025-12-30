import os
from selectors import SelectSelector

from pymongo import MongoClient
from bson import ObjectId

# initial a contact
class Contact:
    def __init__(self, id: str, first_name: str, last_name: str, phone_number: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    # turn object to a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

# Read from environment variables
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "contactsdb")

# Create connection
client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")

# Access database
db = client.MONGO_DB

# Access collection
collection = db.contacts

# create new contact
contact = {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1-555-0105"
}
if collection.find_one({"phone_number": contact["phone_number"]}):
    print("Contact with this phone_number already exists")
else:
    result = collection.insert_one(contact)
    print(f"Inserted ID: {result.inserted_id}")

# update a contact
filter_query = {"_id": ObjectId("6953d5c6306d829f084008b4")}
update_data = {"$set": {"phone_number": "+1-555-0103"}}
if collection.find_one({"phone_number": "+1-555-0103"}):
    print("Contact with this phone_number already exists")
else:
    result = collection.update_one(filter_query, update_data)
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

# delete a contact
result = collection.delete_one({"name": "John Doe"})
print(f"Deleted count: {result.deleted_count}")

# get all contacts
contacts = collection.find()
for contact in contacts:
    print(contact)

# Close Connection
client.close()
