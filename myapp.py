from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, static_url_path='/static')

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskzaq'


# try:
# #     # Create a MySQL connection
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

#     # Check if the connection is successful
#     if mysql.is_connected():
#         print('Connected to MySQL!')
# except mysql.connector.Error as e:
#     print(f"Error: {e}")
#     # Handle the error (e.g., log it, show an error message, etc.)
#     raise  # This will re-raise the exception
# finally:
#     # Close the connection if it was opened
#     if 'mysql' in locals() and mysql.is_connected():
#         mysql.close()
#         print('MySQL connection closed.')


@app.route('/')
def index():
    with mysql.cursor() as cur:
        cur.execute('SELECT * FROM your_table_name')
        data = cur.fetchall()
    return render_template('index.html', data=data)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        details = request.form
        alamat = details.get('alamat')
        fakultas = details.get('fakultas')
        nomer_hp = details.get('nomer_hp')

        # Add data to MySQL
        with mysql.cursor() as cur:
            cur.execute("INSERT INTO your_table_name(alamat, fakultas, nomer_hp) VALUES (%s, %s, %s)",
                        (alamat, fakultas, nomer_hp))
        mysql.commit()

        return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    with mysql.cursor() as cur:
        cur.execute("SELECT * FROM your_table_name WHERE id = %s", (id,))
        data = cur.fetchall()
    return render_template('edit.html', data=data[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        details = request.form
        alamat = details['alamat']
        fakultas = details['fakultas']
        nomer_hp = details['nomer_hp']

        # Update data in MySQL
        with mysql.cursor() as cur:
            cur.execute("UPDATE your_table_name SET alamat = %s, fakultas = %s, nomer_hp = %s WHERE id = %s",
                        (alamat, fakultas, nomer_hp, id))
        mysql.commit()

        return redirect(url_for('index'))


@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    # Delete data from MySQL
    with mysql.cursor() as cur:
        cur.execute("DELETE FROM your_table_name WHERE id = %s", (id,))
    mysql.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
