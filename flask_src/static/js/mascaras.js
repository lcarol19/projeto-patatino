/**
 * mascaras.js — máscaras de entrada e integração com ViaCEP
 * Requisito PI: script web (JavaScript)
 */

/* ── CPF: 000.000.000-00 ────────────────────────────────────── */
function maskCPF(input) {
    let v = input.value.replace(/\D/g, '').slice(0, 11);
    v = v.replace(/(\d{3})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = v;
}

/* ── RG: 00.000.000-X ───────────────────────────────────────── */
function maskRG(input) {
    let v = input.value.replace(/[^0-9xX]/g, '').slice(0, 9).toUpperCase();
    v = v.replace(/(\d{2})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})(\d)/, '$1.$2');
    v = v.replace(/(\d{3})([0-9xX])$/, '$1-$2');
    input.value = v;
}

/* ── Telefone: (00) 00000-0000 ou (00) 0000-0000 ───────────── */
function maskTelefone(input) {
    let v = input.value.replace(/\D/g, '');
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length <= 10) {
        v = v.replace(/^(\d{2})(\d)/, '($1) $2');
        v = v.replace(/(\d{4})(\d)/, '$1-$2');
    } else {
        v = v.replace(/^(\d{2})(\d)/, '($1) $2');
        v = v.replace(/(\d{5})(\d)/, '$1-$2');
    }
    input.value = v;
}

/* ── CEP: 00000-000 ─────────────────────────────────────────── */
function maskCEP(input) {
    let v = input.value.replace(/\D/g, '').slice(0, 8);
    v = v.replace(/(\d{5})(\d)/, '$1-$2');
    input.value = v;
}

/* ── ViaCEP: preenche endereço automaticamente ──────────────── */
async function buscarCEP(input) {
    const cep = input.value.replace(/\D/g, '');
    if (cep.length !== 8) return;

    const feedback = document.getElementById('cep-feedback');
    if (feedback) {
        feedback.textContent = 'Buscando endereço…';
        feedback.className = 'form-text text-muted';
    }

    try {
        const resp = await fetch(`/api/cep/${cep}`);
        if (!resp.ok) throw new Error('CEP não encontrado');

        const dados = await resp.json();

        // Preenche os campos do formulário
        _setVal('endereco',  dados.endereco);
        _setVal('bairro',    dados.bairro);
        _setVal('cidade',    dados.cidade);
        _setVal('estado',    dados.estado);

        if (feedback) {
            feedback.textContent = '✅ Endereço encontrado!';
            feedback.className = 'form-text text-success';
        }

        // Foca no campo número para facilitar preenchimento
        const campoNumero = document.getElementById('numero');
        if (campoNumero) campoNumero.focus();

    } catch (err) {
        if (feedback) {
            feedback.textContent = '❌ CEP não encontrado. Preencha o endereço manualmente.';
            feedback.className = 'form-text text-danger';
        }
    }
}

function _setVal(id, valor) {
    const el = document.getElementById(id);
    if (el && valor) el.value = valor;
}

/* ── Aplica máscaras nos campos ao carregar a página ────────── */
document.addEventListener('DOMContentLoaded', function () {
    const cpf = document.getElementById('cpf');
    if (cpf) cpf.addEventListener('input', () => maskCPF(cpf));

    const rg = document.getElementById('rg');
    if (rg) rg.addEventListener('input', () => maskRG(rg));

    const tel = document.getElementById('telefone');
    if (tel) tel.addEventListener('input', () => maskTelefone(tel));

    const cep = document.getElementById('cep');
    if (cep) {
        cep.addEventListener('input', () => maskCEP(cep));
        cep.addEventListener('blur',  () => buscarCEP(cep));
    }
});
