/**
 * fotos_preview.js — pré-visualização de fotos antes do upload
 * Permite adicionar e remover fotos com limite de 3
 */

const MAX_FOTOS = 3;
let dataTransfer = new DataTransfer();

document.addEventListener('DOMContentLoaded', function () {
    const inputFotos    = document.getElementById('fotos_animal');
    const previewContainer = document.getElementById('preview-fotos');

    if (!inputFotos || !previewContainer) return;

    inputFotos.addEventListener('change', function () {
        // Adiciona arquivos novos ao DataTransfer interno
        Array.from(this.files).forEach(file => {
            if (dataTransfer.files.length < MAX_FOTOS) {
                dataTransfer.items.add(file);
            }
        });
        inputFotos.files = dataTransfer.files;
        renderizarPreviews();
    });

    function renderizarPreviews() {
        previewContainer.innerHTML = '';

        Array.from(dataTransfer.files).forEach((file, index) => {
            const reader = new FileReader();

            reader.onload = function (e) {
                const col = document.createElement('div');
                col.className = 'col-4 col-md-3 position-relative';
                col.innerHTML = `
                    <img src="${e.target.result}"
                         class="foto-preview"
                         alt="Pré-visualização da foto ${index + 1}">
                    <button type="button"
                            class="foto-remove-btn"
                            aria-label="Remover foto ${index + 1}"
                            data-index="${index}">
                        <i class="fa-solid fa-xmark" aria-hidden="true"></i>
                    </button>
                    ${index === 0
                        ? '<span class="badge bg-success position-absolute bottom-0 start-0 m-1">Principal</span>'
                        : ''}
                `;
                previewContainer.appendChild(col);

                // Botão de remover
                col.querySelector('.foto-remove-btn')
                   .addEventListener('click', function () {
                       const idx = parseInt(this.dataset.index);
                       dataTransfer.items.remove(idx);
                       inputFotos.files = dataTransfer.files;
                       renderizarPreviews();
                   });
            };

            reader.readAsDataURL(file);
        });

        // Aviso de limite
        if (dataTransfer.files.length >= MAX_FOTOS) {
            const aviso = document.createElement('div');
            aviso.className = 'col-12';
            aviso.innerHTML = `
                <p class="text-warning small mb-0" role="status" aria-live="polite">
                    <i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>
                    Limite de ${MAX_FOTOS} fotos atingido.
                </p>`;
            previewContainer.appendChild(aviso);
            inputFotos.disabled = true;
        } else {
            inputFotos.disabled = false;
        }
    }
});
