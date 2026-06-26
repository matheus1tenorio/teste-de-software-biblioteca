# 📚 Teste de Software — Sistema de Biblioteca

Sistema de gerenciamento de biblioteca com arquitetura de microsserviços, cobrindo **Cliente**, **Livro** e **Empréstimo**. Este documento descreve como instalar as dependências e executar os testes unitários e de integração do projeto.

---

## 🛠️ Instalação das Dependências

Execute os comandos abaixo para instalar as bibliotecas necessárias:

```bash
python -m pip install flask
python -m pip install pytest
python -m pip install mysql-connector-python
```

---

## 🧪 Testes Unitários

Os testes unitários validam cada camada da aplicação de forma isolada (model, controller e routes), utilizando mocks para simular dependências externas como banco de dados e serviços HTTP.

### Cliente

```bash
python -m pytest tests/unit/test_cliente_controller.py -v
python -m pytest tests/unit/test_cliente_model.py -v
python -m pytest tests/unit/test_cliente_routes.py -v
```

### Livro

```bash
python -m pytest tests/unit/test_livro_controller.py -v
python -m pytest tests/unit/test_livro_model.py -v
python -m pytest tests/unit/test_livro_routes.py -v
```

### Empréstimo

```bash
python -m pytest tests/unit/test_emprestimo_controller.py -v
python -m pytest tests/unit/test_emprestimo_model.py -v
python -m pytest tests/unit/test_emprestimo_routes.py -v
```

---

## 🔗 Testes de Integração

Os testes de integração realizam chamadas HTTP reais aos serviços. Certifique-se de que os três microsserviços estejam rodando antes de executá-los:

| Serviço    | Porta padrão |
|------------|-------------|
| Cliente    | 5001        |
| Livro      | 5002        |
| Empréstimo | 5003        |

### Por serviço

```bash
python -m pytest tests/integration/test_cliente_integration.py -v
python -m pytest tests/integration/test_livro_integration.py -v
python -m pytest tests/integration/test_emprestimo_integration.py -v
```

### Fluxo completo (End-to-End)

Valida o ciclo completo: criação de cliente → cadastro de livro → empréstimo → devolução.

```bash
python -m pytest tests/integration/test_fluxo_completo.py -v
```

---

## ▶️ Executar Todos os Testes de Uma Vez

```bash
python -m pytest tests/ -v
```

---

## 🗂️ Estrutura de Testes

```
tests/
├── unit/
│   ├── test_cliente_controller.py
│   ├── test_cliente_model.py
│   ├── test_cliente_routes.py
│   ├── test_livro_controller.py
│   ├── test_livro_model.py
│   ├── test_livro_routes.py
│   ├── test_emprestimo_controller.py
│   ├── test_emprestimo_model.py
│   └── test_emprestimo_routes.py
└── integration/
    ├── test_cliente_integration.py
    ├── test_livro_integration.py
    ├── test_emprestimo_integration.py
    └── test_fluxo_completo.py
```
