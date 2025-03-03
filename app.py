from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_fontawesome import FontAwesome
import logging

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

# Configurazione del database MySQL tramite variabili d'ambiente
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Inserisci la password corretta
app.config['MYSQL_DB'] = 'python_crud'

mysql = MySQL(app)

# Funzione per verificare la connessione al database
def check_db_connection():
    try:
        conn = mysql.connection
        conn.ping()  # Verifica che la connessione sia ancora attiva
        logging.debug("Connessione al database avvenuta con successo!")
        return True
    except Exception as e:
        logging.error(f"Errore di connessione al database: {str(e)}")
        flash(f"Errore di connessione al database: {str(e)}")
        return False


@app.route('/')
def index():
    try:
        # Verifica la connessione al database
        if mysql.connection:
            logging.debug("Connessione al database stabilita con successo")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM students")
            data = cur.fetchall()
            cur.close()
        else:
            flash("Errore nella connessione al database!")
            logging.error("Connessione al database fallita!")
            return render_template('index.html', students=[])
    except Exception as e:
        flash(f"Errore durante il recupero dei dati: {e}")
        logging.error(f"Errore durante il recupero dei dati: {e}")
        return render_template('index.html', students=[])

    return render_template('index.html', students=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("Tutti i campi sono obbligatori!")
            return redirect(url_for('index'))

        # Controlla se la connessione è valida
        if not mysql.connection:
            flash("Errore nella connessione al database!")
            return redirect(url_for('index'))

        try:
            flash("Dati inseriti con successo!")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students(name, email, phone) VALUES(%s, %s, %s)", (name, email, phone))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(f"Errore durante l'inserimento: {e}")
            return redirect(url_for('index'))

        return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        # Validazione dei dati inviati
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if not name or not email or not phone:
            flash("Please fill in all fields!")
            return redirect(url_for('index'))

        if not check_db_connection():
            return redirect(url_for('index'))

        try:
            flash("Data Updated Successfully")

            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
            """, (name, email, phone, id_data))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            flash(f"Errore durante l'aggiornamento dei dati: {str(e)}")
            return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    if not check_db_connection():
        return redirect(url_for('index'))

    try:
        flash("Data Deleted Successfully")

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        flash(f"Errore durante la cancellazione dei dati: {str(e)}")

    return redirect(url_for('index'))


# Configura il logger
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Verifica se il database è connesso prima di avviare l'app
    if not check_db_connection():
        print("Impossibile connettersi al database. L'app non può essere avviata.")
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
