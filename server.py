import pyodbc as odbc
from flask import Flask, request, jsonify


app = Flask(__name__)

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sql-auth.database.windows.net,1433;Database=account;Uid=admin1;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = odbc.connect(connection_string)

cursor = conn.cursor()


# cursor.execute(sql)
# for row in cursor.columns(table="user_details"):
#     print(row.column_name)
#     for field in row:
#         print(field)
def insert_user_password(username, password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_details (email, password) VALUES (?, ?)",
        username,
        password,
    )
    conn.commit()
    conn.close()


def check_username_password(username, password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user_details WHERE email = ? AND password = ?",
        username,
        password,
    )
    result = cursor.fetchone()
    conn.close()

    return result is not None


def update_password(username, new_password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_details SET password = ? WHERE email = ?", new_password, username
    )
    conn.commit()
    conn.close()
    print("updated Sucessfully")


@app.route("/login", methods=["POST"])
def login():
    print("hi")
    data = request.get_json()  # Get the JSON data from the request
    username = data.get("email")  # Extract username from JSON data
    password = data.get("password")  # Extract password from JSON data
    print(username + "hi")
    if username and password:  # Check if both username and password are provided
        if check_username_password(username, password):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    else:
        return jsonify({"message": "Invalid Input"}), 400


if __name__ == "__main__":
    app.run(debug=True)
