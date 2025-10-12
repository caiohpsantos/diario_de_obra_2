// --- edita_servico.js ---
// Controle de edição inline de serviços padrão

document.addEventListener('DOMContentLoaded', () => {
  // Seleciona todas as linhas que possuem dados
  document.querySelectorAll('tr[data-id]').forEach(row => {
    const btnEditar = row.querySelector('.btn-editar');
    const btnSalvar = row.querySelector('.btn-salvar');
    const spanDescricao = row.querySelector('.descricao-text');
    const inputDescricao = row.querySelector('.descricao-input');

    // Alternar para modo edição
    btnEditar.addEventListener('click', () => {
      spanDescricao.classList.add('d-none');
      inputDescricao.classList.remove('d-none');
      btnEditar.classList.add('d-none');
      btnSalvar.classList.remove('d-none');
      inputDescricao.focus();
    });

    // Salvar alteração via fetch
    btnSalvar.addEventListener('click', () => {
      const novoValor = inputDescricao.value.trim();
      if (novoValor === '') return;

      fetch(window.editaEfetivoUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.csrfToken
        },
        body: JSON.stringify({
          id: row.dataset.id,
          descricao: novoValor
        })
      })
      .then(resp => resp.json())
      .then(data => {
        if (data.sucesso) {
          spanDescricao.textContent = novoValor;
          spanDescricao.classList.remove('d-none');
          inputDescricao.classList.add('d-none');
          btnSalvar.classList.add('d-none');
          btnEditar.classList.remove('d-none');
        } else {
          alert('Erro ao salvar: ' + data.mensagem);
        }
      })
      .catch(err => alert('Erro: ' + err));
    });

    // Pressionar Enter no campo de edição → aciona Salvar
    inputDescricao.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        btnSalvar.click();
      }
    });
  });
});
