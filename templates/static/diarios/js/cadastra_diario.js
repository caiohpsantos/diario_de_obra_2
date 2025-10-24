// lida com o formset de serviços
document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-servico");
  const container = document.getElementById("servicos-container");
  const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

  // Atualiza o campo "item" com a contagem
  const atualizarNumeracao = () => {
    const forms = container.querySelectorAll(".servico-form");
    forms.forEach((form, index) => {
      const itemInput = form.querySelector('input[name$="-item"]');
      if (itemInput) {
        itemInput.value = index + 1;
      }
    });
  };

  // Adiciona novo serviço
  addBtn.addEventListener("click", () => {
    const currentForms = parseInt(totalForms.value);
    if (currentForms >= 14) {
      alert("Você atingiu o limite máximo de 14 serviços.");
      return;
    }

    const newForm = container.querySelector(".servico-form").cloneNode(true);
    newForm.querySelectorAll("input, select").forEach(input => {
      const name = input.name.replace(/-\d+-/, `-${currentForms}-`);
      const id = input.id.replace(/-\d+-/, `-${currentForms}-`);
      input.name = name;
      input.id = id;

      // Limpa valores
      if (input.type !== "hidden") {
        input.value = "";
      }
    });

    container.appendChild(newForm);
    totalForms.value = currentForms + 1;

    atualizarNumeracao();
  });

  // Remove serviço
  container.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-servico")) {
      const formRows = container.querySelectorAll(".servico-form");
      if (formRows.length > 1) {
        e.target.closest(".servico-form").remove();
        totalForms.value = parseInt(totalForms.value) - 1;
        atualizarNumeracao();
      } else {
        alert("É necessário ter pelo menos um serviço.");
      }
    }
  });

  atualizarNumeracao();
});

// Lida com o efetivo direto
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-efetivo-direto");
  const leitura = document.getElementById("efetivo-direto-leitura");
  const edicao = document.getElementById("efetivo-direto-edicao");
  const addBtn = document.getElementById("add-efetivo-direto");
  const totalForms = document.querySelector("#id_efetivo_direto-TOTAL_FORMS");

  // 🔹 Alterna exibição entre leitura e edição
  toggle.addEventListener("change", () => {
    const show = toggle.checked;
    leitura.style.display = show ? "none" : "block";
    edicao.style.display = show ? "block" : "none";
    addBtn.style.display = show ? "inline-block" : "none";
  });

  // 🔹 Atualiza campos "ausente" e "efetivo" dinamicamente
  edicao.addEventListener("input", (e) => {
    if (e.target.name.includes("qtde") || e.target.name.includes("presente")) {
      const form = e.target.closest(".efetivo-form");
      const qtde = form.querySelector(`[name*='qtde']`).value || 0;
      const presente = form.querySelector(`[name*='presente']`).value || 0;
      const ausente = form.querySelector(".ausente");
      const efetivo = form.querySelector(".efetivo");

      ausente.value = Math.max(0, qtde - presente);
      efetivo.value = presente;
    }
  });

  // 🔹 Adicionar novo formulário
  addBtn.addEventListener("click", () => {
    const currentForms = parseInt(totalForms.value);
    const newForm = edicao.querySelector(".efetivo-form").cloneNode(true);

    newForm.querySelectorAll("input").forEach(input => {
      if (input.name) {
        input.name = input.name.replace(/-\d+-/, `-${currentForms}-`);
        input.id = input.id.replace(/-\d+-/, `-${currentForms}-`);
      }
      if (!input.classList.contains("ausente") && !input.classList.contains("efetivo")) {
        input.value = "";
      } else {
        input.value = "";
      }
    });

    edicao.appendChild(newForm);
    totalForms.value = currentForms + 1;
  });

  // 🔹 Remover formulário
  edicao.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-efetivo-direto") || e.target.closest(".remove-efetivo-direto")) {
      const forms = edicao.querySelectorAll(".efetivo-form");
      if (forms.length > 1) {
        e.target.closest(".efetivo-form").remove();
        totalForms.value = parseInt(totalForms.value) - 1;
      } else {
        alert("Deve haver pelo menos um registro de efetivo direto.");
      }
    }
  });
});


// 🔹 Aciona o botão "Adicionar Serviço" ao pressionar Enter no campo de referência
document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("servicos-container");
  const addBtn = document.getElementById("add-servico");

  if (container && addBtn) {
    container.addEventListener("keydown", (event) => {
      const isReferencia = event.target.name && event.target.name.includes("referencia");
      if (isReferencia && event.key === "Enter") {
        event.preventDefault();
        addBtn.click();
      }
    });
  }
});


// Lida com o formulário de Efetivo Indireto
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-efetivo-indireto");
  const leitura = document.getElementById("efetivo-indireto-leitura");
  const edicao = document.getElementById("efetivo-indireto-edicao");
  const addBtnContainer = document.getElementById("add-efetivo-indireto-container");
  const addBtn = document.getElementById("add-efetivo-indireto");
  const totalForms = document.querySelector("#id_efetivo_indireto-TOTAL_FORMS");

  // 🔹 Alterna exibição entre leitura e edição
  toggle.addEventListener("change", () => {
    const show = toggle.checked;
    leitura.style.display = show ? "none" : "block";
    edicao.style.display = show ? "block" : "none";
    addBtnContainer.style.display = show ? "block" : "none";
  });

  // 🔹 Adicionar novo formulário
  addBtn.addEventListener("click", () => {
    const currentForms = parseInt(totalForms.value);
    const newForm = edicao.querySelector(".efetivo-indireto-form").cloneNode(true);

    // Atualiza índices e limpa valores
    newForm.querySelectorAll("input, select").forEach(input => {
      if (input.name) {
        input.name = input.name.replace(/-\d+-/, `-${currentForms}-`);
        input.id = input.id.replace(/-\d+-/, `-${currentForms}-`);
      }
      input.value = "";
    });

    edicao.appendChild(newForm);
    totalForms.value = currentForms + 1;
  });

  // 🔹 Pressionar Enter no campo "efetivo" adiciona nova função
  edicao.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && event.target.name && event.target.name.includes("efetivo")) {
      event.preventDefault(); // Evita envio do formulário
      addBtn.click();         // Simula o clique no botão de adicionar
    }
  });

  // 🔹 Remover formulário
  edicao.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-efetivo-indireto") || e.target.closest(".remove-efetivo-indireto")) {
      const forms = edicao.querySelectorAll(".efetivo-indireto-form");
      if (forms.length > 1) {
        e.target.closest(".efetivo-indireto-form").remove();
        totalForms.value = parseInt(totalForms.value) - 1;
      } else {
        alert("Deve haver pelo menos um registro de efetivo indireto.");
      }
    }
  });
});
