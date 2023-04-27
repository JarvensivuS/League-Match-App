from flask import Flask, render_template, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

connect = sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS games (gameid INTEGER not NULL PRIMARY KEY,sport TEXT, \
    team1 TEXT, team2 TEXT, score1 INTEGER, score2 INTEGER,gamedate DATE)')

@app.route('/', methods=['POST','GET'])

def addFormInput():

    if request.method == 'POST':
        gameid = request.form['gameid']
        sport = request.form['sport']
        team1 = request.form['team1']
        team2 = request.form['team2']
        score1 = request.form['score1']
        score2 = request.form['score2']
        gamedate = request.form['gamedate']
        
        with sqlite3.connect("database.db") as games:
            cursor = games.cursor()

            
            cursor.execute("SELECT gameid FROM games WHERE gameid=?",(gameid))
            dbResult = cursor.fetchone()
            
            #Check for an existing gameid
            if dbResult:
                flash('Game id '+gameid+' already used! Try again.')
            else:
                cursor.execute("INSERT INTO games \
                (gameid,sport,team1,team2,score1,score2,gamedate) VALUES (?,?,?,?,?,?,?)",
                (gameid, sport, team1, team2, score1,score2,gamedate))
                games.commit()
            
            cursor.execute('SELECT * FROM games')
            
        return render_template("index.html", data=cursor.fetchall())
    
    #Handle GET method on page load to fill table.
    else:
        connect = sqlite3.connect('database.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM games')
        return render_template("index.html", data=cursor.fetchall()) 

   
if __name__ == '__main__':
    app.run(debug=False)