from flask import Flask, render_template, request
import re

app = Flask(__name__)

def validar_regex(pattern):
    try:
        re.compile(pattern)
        return True, ""
    except re.error as e:
        return False, str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    coincidencias = []
    regex = ""
    texto = ""

    if request.method == "POST":
        regex = request.form["regex"]
        texto = request.form["texto"]

        valido, error = validar_regex(regex)
        if not valido:
            resultado = f"Error: {error}"
        else:
            coincidencias = re.findall(regex, texto)
            resaltado = re.sub(
                f"({regex})", r"<mark>\1</mark>", texto
            )
            resultado = resaltado

    return render_template(
        "index.html", 
        resultado=resultado, 
        coincidencias=coincidencias, 
        regex=regex, 
        texto=texto
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

