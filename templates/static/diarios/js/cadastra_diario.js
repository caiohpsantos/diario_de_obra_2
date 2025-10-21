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

// lida com o formset de efetivo direto
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-efetivo");
  const container = document.getElementById("efetivo-container");
  const addBtn = document.getElementById("add-efetivo");
  const totalForms = document.querySelector("#id_efetivo-TOTAL_FORMS");

  toggle.addEventListener("change", () => {
    const show = toggle.checked;
    container.style.display = show ? "block" : "none";
    addBtn.style.display = show ? "inline-block" : "none";
  });

  addBtn.addEventListener("click", () => {
    const currentForms = parseInt(totalForms.value);
    const newForm = container.querySelector(".efetivo-form").cloneNode(true);

    newForm.querySelectorAll("input").forEach(input => {
      input.name = input.name.replace(/-\d+-/, `-${currentForms}-`);
      input.id = input.id.replace(/-\d+-/, `-${currentForms}-`);
      input.value = "";
    });

    container.appendChild(newForm);
    totalForms.value = currentForms + 1;
  });

  container.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-efetivo")) {
      const forms = container.querySelectorAll(".efetivo-form");
      if (forms.length > 1) {
        e.target.closest(".efetivo-form").remove();
        totalForms.value = parseInt(totalForms.value) - 1;
      }
    }
  });
});



