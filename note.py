


# Define the Ticket Schema:

ticket_schema = {
    "date_of_validity": datetime.datetime,
    "seat_number": str,
    "price": float,
    "concert_id": ObjectId  # Reference to the concert document
}

# Create Tickets for a concert:

# Assuming you have the concert_id and ticket_data containing ticket details
ticket_data["concert_id"] = ObjectId(concert_id)
tickets_collection.insert_one(ticket_data)


# Retrieve tickets for a concert
concert_tickets = tickets_collection.find({"concert_id": ObjectId(concert_id)})


# Perform Ticket Validations

ticket = tickets_collection.find_one({"_id": ObjectId(ticket_id)})
if ticket:
    # Validate ticket date
    if ticket["date_of_validity"] < datetime.datetime.now():
        print("Ticket has expired.")
        return

    # Check seat availability
    concert = concerts_collection.find_one({"_id": ticket["concert_id"]})
    if concert["capacity"] <= 0:
        print("No seats available for the concert.")
        return

    # Decrement the seat count for the concert
    concerts_collection.update_one({"_id": ticket["concert_id"]}, {"$inc": {"capacity": -1}})
    print("Ticket validated. Enjoy the concert!")
else:
    print("Ticket not found.")


# --------------

# Check if user is registered
#if users_coll.find({"Username": user}).count() == 0:
#    raise ValueError("Utente non registrato")