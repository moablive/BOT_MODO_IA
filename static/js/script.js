document.addEventListener('DOMContentLoaded', carregarRegistros);
const modalEl = document.getElementById('registroModal');
const modal = new bootstrap.Modal(modalEl);

function mostrarAlerta(mensagem, tipo) {
    const container = document.getElementById('alert-container');
    container.innerHTML = `<div class="alert alert-${tipo} alert-dismissible fade show">${mensagem}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

async function carregarRegistros() {
    try {
        const res = await fetch('/api/registros');
        const dados = await res.json();
        const tbody = document.getElementById('tabela-corpo');
        tbody.innerHTML = '';
        dados.forEach(reg => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${reg.id}</td><td>${reg.nome}</td><td>${reg.telefone}</td>
            <td><span class="badge bg-info text-dark">${reg.modo_ia}</span></td>
            <td class="text-end">
                <button class="btn btn-sm btn-primary action-btn" onclick="editarRegistro(${reg.id}, '${reg.nome}', '${reg.telefone}', '${reg.modo_ia}')">✏️</button>
                <button class="btn btn-sm btn-danger action-btn" onclick="deletarRegistro(${reg.id})">🗑️</button>
            </td>`;
            tbody.appendChild(tr);
        });
    } catch (err) { console.error(err); }
}

function limparFormulario() {
    document.getElementById('registroId').value = '';
    document.getElementById('nome').value = '';
    document.getElementById('telefone').value = '';
    document.getElementById('modo_ia').value = 'Ativado';
    document.getElementById('modalTitle').innerText = 'Novo Registro';
}

function editarRegistro(id, nome, telefone, modoIa) {
    document.getElementById('registroId').value = id;
    document.getElementById('nome').value = nome;
    document.getElementById('telefone').value = telefone;
    document.getElementById('modo_ia').value = modoIa;
    document.getElementById('modalTitle').innerText = 'Editar Registro';
    modal.show();
}

async function salvarRegistro() {
    const id = document.getElementById('registroId').value;
    const dados = {
        nome: document.getElementById('nome').value,
        telefone: document.getElementById('telefone').value,
        modo_ia: document.getElementById('modo_ia').value
    };
    const url = id ? `/api/registro/${id}` : '/api/registro';
    const method = id ? 'PUT' : 'POST';
    try {
        const res = await fetch(url, { method: method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) });
        if (res.ok) { mostrarAlerta('Sucesso!', 'success'); modal.hide(); carregarRegistros(); }
        else { const err = await res.json(); mostrarAlerta(err.error, 'danger'); }
    } catch (err) { mostrarAlerta('Erro ao salvar.', 'danger'); }
}

async function deletarRegistro(id) {
    if (!confirm('Excluir?')) return;
    try {
        const res = await fetch(`/api/registro/${id}`, { method: 'DELETE' });
        if (res.ok) { carregarRegistros(); }
    } catch (err) { alert('Erro'); }
}