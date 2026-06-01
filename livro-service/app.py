from flask import Flask
from flask_cors import CORS
from routes.livro_routes import livro_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(livro_bp)

@app.route("/")
def home():
    return {"mensagem": "Livro Service rodando"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)