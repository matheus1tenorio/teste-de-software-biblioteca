from flask import Flask
from flask_cors import CORS
from src.emprestimo_service.routes.emprestimo_routes import emprestimo_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(emprestimo_bp)

@app.route("/")
def home():
    return {"mensagem": "Emprestimo Service rodando"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)