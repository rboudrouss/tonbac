# codé par cyber vladimir poutine et Rboud-sensei
from flask import Flask, render_template, request
from math import ceil

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/calcul', methods=['POST', 'GET'])
def calcul():
    # POST CASE
    if request.method == "POST":
        # déclaration & assignation
        notes = []
        FR_ecrit = ceil(float(request.form["FR_ecrit"]))
        FR_oral = ceil(float(request.form["FR_oral"]))
        TPE = ceil(float(request.form["TPE"]))
        TPE = (TPE-10) if TPE>10 else 0
        try:
            oib = request.form["oib"] == "on"
        except:
            oib = False
        spe = request.form["spe"]
        for i in range(1, 3):
            for j in ["sport", "philo", "phch", "svt", "math", "lv1", "hg", "lv2", "spe", "option"]:
                notes.append(ceil(float(request.form[j + str(i)])))
        if not notes[9]:
            option = False
        else:
            option = True
        
        # les coefs de base sans spé
        coefs = [2, 3, 6, 6, 7, 3, 3]

        # application des coefficients selon les réponses
        if spe == "M":
            coefs[4] = 9
        elif spe == "P":
            coefs[2] = 8
        elif spe == "S":
            coefs[3] = 8
        if oib:
            coefs[5:7] = [9, 7]

        # moyenne par matière
        moyenne_m = []
        for i in range(len(notes) // 2 + 1):
            try:
                moyenne_m.append((notes[i] + notes[i + 10]) / 2)
            except:
                break
        
        # calcul
        somme_des_coefs = coefs[0] * 3 + coefs[1] + \
            coefs[2] + coefs[3] + coefs[4] + coefs[5] + coefs[6]
        if option:
            moyenne_tot = (moyenne_m[4] * coefs[4] + moyenne_m[2] * coefs[2] + moyenne_m[3] * coefs[3] + moyenne_m[6] * coefs[6] + moyenne_m[5] * coefs[5] + moyenne_m[7] * coefs[0] +
                           moyenne_m[1] * coefs[1] + FR_oral * coefs[0] + FR_ecrit * coefs[0] + TPE * coefs[0] + ((moyenne_m[9] - 10) if moyenne_m[9] > 10 else 0) * coefs[0] + moyenne_m[0] * coefs[0]) / somme_des_coefs
        else:
            moyenne_tot = (moyenne_m[4] * coefs[4] + moyenne_m[2] * coefs[2] + moyenne_m[3] * coefs[3] + moyenne_m[6] * coefs[6] + moyenne_m[5] * coefs[5] + moyenne_m[7] * coefs[0] +
                           moyenne_m[1] * coefs[1] + FR_oral * coefs[0] + FR_ecrit * coefs[0] + TPE * coefs[0] + moyenne_m[0] * coefs[0]) / somme_des_coefs
        return render_template("result.html", res=str(moyenne_tot)[:5])
    
    # page visite
    else:
        return render_template("calcul.html")


@app.route('/<a>')
def lost(a):
    return render_template("notf.html", a=a)


if __name__ == '__main__':
    app.run(debug=True)
