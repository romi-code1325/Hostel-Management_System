import sqlite3
import os

DATABASE = os.path.join(
    "instance",
    "hostel.db"
)

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

try:

    cursor.execute(
        "ALTER TABLE room ADD COLUMN image VARCHAR(200)"
    )

    print("✅ Image column added successfully!")

except sqlite3.OperationalError as e:

    if "duplicate column name" in str(e).lower():

        print("ℹ️ Image column already exists.")

    else:

        print("❌ Error:", e)
        connection.close()
        exit()


cursor.execute(
    """
    UPDATE room
    SET image = 'room1.jpg'
    WHERE image IS NULL
    """
)

connection.commit()

connection.close()

print("✅ Database update completed!")