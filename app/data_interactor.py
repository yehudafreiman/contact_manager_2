import os
from pymongo import MongoClient
from bson import ObjectId


# initial a contact
class Contact:
    def __init__(self, contact_id: str, first_name: str, last_name: str, phone_number: str):
        self.contact_id = contact_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    # turn object to a dictionary
    def to_dict(self):
        return {
            "id": self.contact_id,
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
db = client[MONGO_DB]
collection = db.contacts


# create new contact
def create_contact(contact_data: dict) -> str:
    if collection.find_one({"phone_number": contact_data["phone_number"]}):
        return "Contact with this phone_number already exists"
    new_contact = collection.insert_one(contact_data)
    return str(new_contact.inserted_id)


# update a contact
def update_contact(contact_id: str, contact_data: dict) -> bool:
    new_phone = contact_data.get("phone_number")
    if new_phone and collection.find_one({"phone_number": new_phone}):
        print("Contact with this phone_number already exists")
        return False
    result = collection.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": contact_data}
    )
    return result.matched_count > 0


# delete a contact
def delete_contact(contact_id: str):
    result = collection.delete_one({"_id": ObjectId(contact_id)})
    return result.deleted_count > 0


# get all contacts
def get_all_contacts() -> list:
    results = collection.find()
    contacts = [Contact(contact_id=str(contact["_id"]),
                        first_name=contact["first_name"],
                        last_name=contact["last_name"],
                        phone_number=contact["phone_number"])
                for contact in results]
    return contacts


