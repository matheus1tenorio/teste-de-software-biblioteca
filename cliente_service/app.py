from flask import Flask
from flask_cors import CORS
from cliente_service.routes.cliente_routes import cliente_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(cliente_bp)

@app.route("/")
def home():
    return {"mensagem": "Cliente Service rodando"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)