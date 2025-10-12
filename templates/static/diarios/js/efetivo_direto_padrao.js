document.addEventListener("DOMContentLoaded", () => {

  // ======== EDIÇÃO INLINE NA TABELA ========
  document.querySelectorAll("tr[data-id]").forEach(row => {
    const btnEditar = row.querySelector(".btn-editar");
    const btnSalvar = row.querySelector(".btn-salvar");

    const spanFuncao = row.querySelector(".descricao-text");
    const inputFuncao = row.querySelector(".descricao-input");

    const spanQtde = row.querySelector(".qtde-text");
    const inputQtde = row.querySelector(".qtde-input");

    const spanPresente = row.querySelector(".presente-text");
    const inputPresente = row.querySelector(".presente-input");

    const spanAusente = row.querySelector(".ausente-text");
    const inputAusente = row.querySelector(".ausente-input");

    const spanEfetivo = row.querySelector(".efetivo-text");
    const inputEfetivo = row.querySelector(".efetivo-input");

    function recalcular() {
      if (!inputQtde.classList.contains('d-none') && !inputPresente.classList.contains('d-none')) {
        let qtde = parseInt(inputQtde.value) || 0;
        let presente = parseInt(inputPresente.value) || 0;

        if (qtde < 1) qtde = 1;
        if (presente < 1) presente = 1;
        if (presente > qtde) presente = qtde;

        inputQtde.value = qtde;
        inputPresente.value = presente;
        inputAusente.value = qtde - presente;
        inputEfetivo.value = presente;
      }
    }

    // Recalcular enquanto digita
    inputQtde.addEventListener("input", recalcular);
    inputPresente.addEventListener("input", recalcular);

    // Pressionar Enter → clicar em Salvar
    inputPresente.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        btnSalvar.click();
      }
    });

    // Entrar no modo de edição
    btnEditar.addEventListener("click", () => {
      [spanFuncao, spanQtde, spanPresente, spanAusente, spanEfetivo].forEach(span => span.classList.add("d-none"));
      [inputFuncao, inputQtde, inputPresente, inputAusente, inputEfetivo].forEach(input => input.classList.remove("d-none"));
      btnEditar.classList.add("d-none");
      btnSalvar.classList.remove("d-none");
      inputFuncao.focus();
      recalcular(); // inicializa valores ao entrar em edição
    });

    // Salvar alteração
    btnSalvar.addEventListener("click", () => {
      const novaFuncao = inputFuncao.value.trim();
      const novaQtde = inputQtde.value.trim();
      const novoPresente = inputPresente.value.trim();

      if (!novaFuncao) { alert("A função não pode ficar vazia."); return; }

      fetch(window.editaEfetivoUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": window.csrfToken },
        body: JSON.stringify({ id: row.dataset.id, funcao: novaFuncao, qtde: novaQtde, presente: novoPresente })
      })
      .then(resp => resp.json())
      .then(data => {
        if (data.sucesso) {
          spanFuncao.textContent = novaFuncao;
          spanQtde.textContent = novaQtde;
          spanPresente.textContent = novoPresente;
          spanAusente.textContent = inputAusente.value;
          spanEfetivo.textContent = inputEfetivo.value;

          [spanFuncao, spanQtde, spanPresente, spanAusente, spanEfetivo].forEach(span => span.classList.remove("d-none"));
          [inputFuncao, inputQtde, inputPresente, inputAusente, inputEfetivo].forEach(input => input.classList.add("d-none"));

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
  const qtdeInput = document.getElementById("qtdeId");
  const presenteInput = document.getElementById("presenteId");
  const ausenteInput = document.getElementById("ausenteId");
  const efetivoInput = document.getElementById("efetivoId");
  const btnAdicionar = document.getElementById("btnAdicionar");

  function calcularAusentes() {
    let qtde = Number(qtdeInput.value) || 0;
    let presente = Number(presenteInput.value) || 0;

    if (qtde < 1) { qtdeInput.value = 1; qtde = 1; }
    if (presente < 1) { presenteInput.value = 1; presente = 1; }
    if (presente > qtde) { presenteInput.value = qtde; presente = qtde; }

    ausenteInput.value = qtde - presente;
    efetivoInput.value = presente;
  }

  qtdeInput.addEventListener("input", calcularAusentes);
  presenteInput.addEventListener("input", calcularAusentes);
  presenteInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") { event.preventDefault(); btnAdicionar.click(); }
  });
  calcularAusentes();
});
