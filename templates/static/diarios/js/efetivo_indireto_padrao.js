document.addEventListener("DOMContentLoaded", () => {

  // ======== EDIÇÃO INLINE NA TABELA ========
  document.querySelectorAll("tr[data-id]").forEach(row => {
    const btnEditar = row.querySelector(".btn-editar");
    const btnSalvar = row.querySelector(".btn-salvar");

    const spanFuncao = row.querySelector(".funcao-text");
    const inputFuncao = row.querySelector(".funcao-input");

    const spanEfetivo = row.querySelector(".efetivo-text");
    const inputEfetivo = row.querySelector(".efetivo-input");

    // Pressionar Enter → clicar em Salvar
    inputEfetivo.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        btnSalvar.click();
      }
    });

    // Entrar no modo de edição
    btnEditar.addEventListener("click", () => {
      [spanFuncao, spanEfetivo].forEach(span => span.classList.add("d-none"));
      [inputFuncao, inputEfetivo].forEach(input => input.classList.remove("d-none"));
      btnEditar.classList.add("d-none");
      btnSalvar.classList.remove("d-none");
      inputFuncao.focus();
      
    });

    // Salvar alteração
    btnSalvar.addEventListener("click", () => {
      const novaFuncao = inputFuncao.value.trim();
      const novoEfetivo = inputEfetivo.value.trim();

      if (!novaFuncao) { alert("A função não pode ficar vazia."); return; }

      fetch(window.editaEfetivoUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": window.csrfToken },
        body: JSON.stringify({ id: row.dataset.id, funcao: novaFuncao, efetivo: novoEfetivo })
      })
      .then(resp => resp.json())
      .then(data => {
        if (data.sucesso) {
          spanFuncao.textContent = novaFuncao;
          spanEfetivo.textContent = inputEfetivo.value;

          [spanFuncao, spanEfetivo].forEach(span => span.classList.remove("d-none"));
          [inputFuncao, inputEfetivo].forEach(input => input.classList.add("d-none"));

          btnSalvar.classList.add("d-none");
          btnEditar.classList.remove("d-none");
        } else {
          alert("Erro ao salvar: " + data.mensagem);
        }
      })
      .catch(err => alert("Erro: " + err));
    });
  });

  // ======== FORMULÁRIO DE CADASTRO RÁPIDO ========
  const funcaoInput = document.getElementById("funcaoId");
  const efetivoInput = document.getElementById("efetivoId");
  const btnAdicionar = document.getElementById("btnAdicionar");

  efetivoInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") { event.preventDefault(); btnAdicionar.click(); }
  });
  
});
