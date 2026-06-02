const API_URL = "/api/clientes";
let editandoId = null;

// ── Carregar e renderizar tabela ───────────────────────────────────────────

async function carregarClientes() {
    try {
        const res = await fetch(API_URL);
        const clientes = await res.json();
        const tbody = document.getElementById('tabela-clientes-body');
        tbody.innerHTML = '';

        if (!clientes.length) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">Nenhum usuário cadastrado.</td></tr>';
            return;
        }

        clientes.forEach(c => {
            tbody.innerHTML += `
                <tr>
                    <td>${c.nome}</td>
                    <td>${c.email}</td>
                    <td>${c.matricula || '-'}</td>
                    <td>
                        <button onclick="prepararEdicao(${c.id}, '${esc(c.nome)}', '${esc(c.email)}', '${esc(c.matricula || '')}')">Editar</button>
                        <button onclick="deletarCliente(${c.id})" style="background:#e74c3c">Excluir</button>
                    </td>
                </tr>`;
        });
    } catch (err) {
        console.error('Erro ao carregar clientes:', err);
        document.getElementById('tabela-clientes-body').innerHTML =
            '<tr><td colspan="4" style="color:red;text-align:center">Erro ao conectar com o serviço de usuários.</td></tr>';
    }
}

// ── Salvar (criar ou atualizar) ────────────────────────────────────────────

async function salvarCliente(e) {
    e.preventDefault();
    const form = e.target;
    const dados = {
        nome:      form.nome_usuario.value.trim(),
        email:     form.email_usuario.value.trim(),
        matricula: form.matricula.value.trim()
    };

    const url    = editandoId ? `${API_URL}/${editandoId}` : API_URL;
    const metodo = editandoId ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: metodo,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        const data = await res.json();
        if (!res.ok) { alert(data.erro || 'Erro ao salvar usuário.'); return; }
        cancelarEdicao();
        carregarClientes();
    } catch (err) {
        alert('Erro ao conectar com o serviço de usuários.');
    }
}

// ── Preparar edição ────────────────────────────────────────────────────────

function prepararEdicao(id, nome, email, matricula) {
    editandoId = id;
    const form = document.getElementById('usuario-form');
    form.nome_usuario.value  = nome;
    form.email_usuario.value = email;
    form.matricula.value     = matricula;

    document.getElementById('form-titulo').innerText       = 'Editar Usuário';
    document.getElementById('btn-salvar').innerText        = 'Atualizar Usuário';
    document.getElementById('btn-cancelar').style.display = 'inline-block';

    form.scrollIntoView({ behavior: 'smooth' });
}

function cancelarEdicao() {
    editandoId = null;
    document.getElementById('usuario-form').reset();
    document.getElementById('form-titulo').innerText       = 'Cadastrar Novo Usuário';
    document.getElementById('btn-salvar').innerText        = 'Cadastrar Usuário';
    document.getElementById('btn-cancelar').style.display = 'none';
}

// ── Excluir ────────────────────────────────────────────────────────────────

async function deletarCliente(id) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return;
    try {
        const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (!res.ok) { alert(data.erro || 'Erro ao excluir usuário.'); return; }
        carregarClientes();
    } catch (err) {
        alert('Erro ao conectar com o serviço de usuários.');
    }
}

// ── Utilitário ─────────────────────────────────────────────────────────────

function esc(str) {
    return String(str || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
}

// ── Init ───────────────────────────────────────────────────────────────────

document.getElementById('usuario-form').addEventListener('submit', salvarCliente);
carregarClientes();
