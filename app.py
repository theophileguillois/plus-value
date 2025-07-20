from flask import Flask, render_template, request
from bdd import inserer_acquisition, recuperer_acquisitions
from decimal import *

app = Flask(__name__)

@app.route("/")
def racine():
	return render_template('index.html')

@app.route("/formulaire", methods=['GET', 'POST'])
def formulaire():
	if request.method == "POST":
		donnees = request.form
		quantite_BTC = float(donnees.get('nbr_BTC_acquis'))
		montant_EUR = float(donnees.get('montant_brut_achat'))
		inserer_acquisition(quantite_BTC, montant_EUR)

	return render_template('formulaire.html', liste_acquisitions=recuperer_acquisitions())

@app.route("/resultat", methods=['GET', 'POST'])
def resultat():
	if request.method == "POST":
		donnees = request.form
		cession = Decimal(float(donnees.get('montant_brut_vente'))) - Decimal(float(donnees.get('frais_vente_EUR')))
		somme_acquisitions_BTC = 0
		somme_acquisitions_EUR = 0
		acquisitions = recuperer_acquisitions()
		for acquisition in acquisitions:
			somme_acquisitions_BTC += acquisition[0]
			somme_acquisitions_EUR += acquisition[1]

		# On calcule une quatrième proportionnelle : 1 EUR * 1 BTC / 1 EUR en BTC
		prix_1_BTC_en_EUR = Decimal(1) / Decimal(str(donnees.get('prix_1_EUR_en_BTC')))

		portefeuille = Decimal(somme_acquisitions_BTC) * Decimal(prix_1_BTC_en_EUR)

		plus_value_totale = Decimal(str(cession)) - Decimal(str(somme_acquisitions_EUR)) * (Decimal(str(cession)) / Decimal(str(portefeuille)))

	return render_template("formulaire.html", plus_value=plus_value_totale, liste_acquisitions=recuperer_acquisitions())
