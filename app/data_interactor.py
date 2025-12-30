import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# initial a contact
class Contact:
    def __init__(self, id: int, first_name: str, last_name: str, phone_number: str):
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


# create database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "mysqlmysql"),
        database=os.getenv("DB_NAME", "contacts")
    )
    return connection


# create new contact
def create_contact(contact_data: dict) -> int:
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """INSERT INTO contacts (first_name, last_name, phone_number) \
               VALUES (%s, %s, %s)"""
    cursor.execute(query, (
        contact_data["first_name"],
        contact_data["last_name"],
        contact_data["phone_number"]
    ))

    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


# get all contacts
def get_all_contacts() -> list[Contact]:
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT id, first_name, last_name, phone_number FROM contacts"
    cursor.execute(query)

    results = cursor.fetchall()
    contacts = [Contact(id=row[0], first_name=row[1], last_name=row[2], phone_number=row[3]) for row in results]

    cursor.close()
    connection.close()
    return contacts


# update a contact
def update_contact(contact_id: str, contact_data: dict) -> bool:
    connection = get_db_connection()
    cursor = connection.cursor()

    updates = []
    params = []

    # Build dynamic UPDATE query based on provided fields
    if "first_name" in contact_data and contact_data["first_name"] is not None:
        updates.append("first_name = %s")
        params.append(contact_data["first_name"])
    if "last_name" in contact_data and contact_data["last_name"] is not None:
        updates.append("last_name = %s")
        params.append(contact_data["last_name"])
    if "phone_number" in contact_data and contact_data["phone_number"] is not None:
        updates.append("phone_number = %s")
        params.append(contact_data["phone_number"])

    if not updates:
        cursor.close()
        connection.close()
        return False

    params.append(contact_id)

    query = f"UPDATE contacts SET {', '.join(updates)} WHERE id = %s"
    cursor.execute(query, params)

    connection.commit()
    success = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return success


# delete a contact
def delete_contact(contact_id: str) -> bool:
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM contacts WHERE id = %s"
    cursor.execute(query, (contact_id,))

    connection.commit()
    success = cursor.rowcount > 0
    cursor.close()
    connection.close()
    return success


# import os
# from pymongo import MongoClient
#
# # Read from environment variables (set in Kubernetes Pod)
#
# MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
#
# MONGO_PORT = os.getenv("MONGO_PORT", "27017")
#
# MONGO_DB = os.getenv("MONGO_DB", "contactsdb")
#
# # Create connection
#
# client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
#
# db = client[MONGO_DB]
#
# contacts_collection = db["contacts"]
#
# Converting ObjectId for API responses:
#
# from bson import ObjectId
#
# def contact_to_dict(contact):
#     return {
#
#             "id": str(contact\["\_id"\]),   \  # Convert ObjectId to string
#
#             "first\_name": contact\["first\_name"\],
#
#             "last\_name": contact\["last\_name"\],
#
#             "phone\_number": contact\["phone\_number"\]
#
#             }