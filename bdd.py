import sqlite3

nom_table = "impot.db"

def creer_table(nom:str):
	con = sqlite3.connect(nom)
	cur = con.cursor()
	cur.execute("""CREATE TABLE acquisitions(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nbr_BTC REAL,
		montant_brut_EUR REAL)""")
	con.close()

#creer_table(nom_table)

def inserer_acquisition(quantite_BTC:float, montant_EUR:float):
	con = sqlite3.connect(nom_table)
	cur = con.cursor()
	cur.execute("""INSERT INTO acquisitions(nbr_BTC, montant_brut_EUR)
		VALUES(?, ?)""", (quantite_BTC, montant_EUR))
	con.commit()
	con.close()

#inserer_acquisition(0.002579, 150)

def recuperer_acquisitions():
	con = sqlite3.connect(nom_table)
	cur = con.cursor()
	res = cur.execute("SELECT nbr_BTC, montant_brut_EUR FROM acquisitions")
	acquisitions = res.fetchall()
	con.close()
	return acquisitions

print(recuperer_acquisitions())
