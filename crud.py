import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")
conn.commit()


# 🔹 Insert Record
def insert_record():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")

    cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                   (name, age, course))
    conn.commit()
    print("✅ Record Inserted Successfully\n")


# 🔹 Display Records
def display_records():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    if len(records) == 0:
        print("⚠️ No records found\n")
    else:
        print("\n--- Student Records ---")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Course: {row[3]}")
        print()


# 🔹 Update Record
def update_record():
    student_id = int(input("Enter ID to update: "))
    name = input("Enter New Name: ")
    age = int(input("Enter New Age: "))
    course = input("Enter New Course: ")

    cursor.execute("""
    UPDATE students 
    SET name = ?, age = ?, course = ?
    WHERE id = ?
    """, (name, age, course, student_id))

    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Record not found\n")
    else:
        print("✅ Record Updated Successfully\n")


# 🔹 Delete Record
def delete_record():
    student_id = int(input("Enter ID to delete: "))

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Record not found\n")
    else:
        print("✅ Record Deleted Successfully\n")


# 🔹 Menu-driven Program
while True:
    print("===== STUDENT DATABASE MENU =====")
    print("1. Insert Record")
    print("2. Display Records")
    print("3. Update Record")
    print("4. Delete Record")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        insert_record()
    elif choice == '2':
        display_records()
    elif choice == '3':
        update_record()
    elif choice == '4':
        delete_record()
    elif choice == '5':
        print("👋 Exiting Program...")
        break
    else:
        print("❌ Invalid Choice\n")

# Close connection
conn.close()