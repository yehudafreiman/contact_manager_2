from fastapi import FastAPI, HTTPException
import data_interactor
import models

app = FastAPI(title="Contact Manager API")


# POST - create new contact
@app.post("/contacts")
def create_new_contact(contact: models.ContactCreate):
    try:
        contact_dict = contact.model_dump()
        new_id = data_interactor.create_contact(contact_dict)
        return {"message": "Contact created successfully", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET - get all contacts
@app.get("/contacts")
def get_all_contacts():
    contacts = data_interactor.get_all_contacts()
    return [contact.to_dict() for contact in contacts]


# PUT - update existing contact
@app.put("/contacts/{contact_id}")
def update_existing_contact(contact_id: int, update: models.ContactUpdate):
    update_dict = update.model_dump(exclude_none=True)

    success = data_interactor.update_contact(contact_id, update_dict)

    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact updated successfully"}


# DELETE - delete contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    success = data_interactor.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}