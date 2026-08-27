import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

from database.database import get_db, init_db, utc_now


load_dotenv()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError(
        "ADMIN_USERNAME and ADMIN_PASSWORD are required."
    )


init_db()

db = get_db()

existing_admin = db.admins.find_one({
    "username": ADMIN_USERNAME
})


if existing_admin:

    db.admins.update_one(
        {"_id": existing_admin["_id"]},
        {
            "$set": {
                "password": generate_password_hash(
                    ADMIN_PASSWORD
                )
            }
        }
    )

    print("Admin password updated successfully.")

else:

    db.admins.insert_one({
        "username": ADMIN_USERNAME,
        "password": generate_password_hash(
            ADMIN_PASSWORD
        ),
        "created_at": utc_now()
    })

    print("Admin account created successfully.")