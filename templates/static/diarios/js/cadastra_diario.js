// 🔹 Função auxiliar para aplicar caixa alta em todos os inputs de texto
function aplicarUppercase(container = document) {
  container.querySelectorAll("input[type='text']").forEach(input => {
    // Evita listeners duplicados
    input.removeEventListener("input", input._upperListener);
    input._upperListener = () => {
      input.value = input.value.toUpperCase();
    };
    input.addEventListener("input", input._upperListener);
  });
}

// lida com o formset de serviços
document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-servico");
  const container = document.getElementById("servicos-container");
  const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

  if (!addBtn || !container || !totalForms) return; // proteção

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

    const prototype = container.querySelector(".servico-form");
    if (!prototype) return;

    const newForm = prototype.cloneNode(true);
    newForm.querySelectorAll("input, select").forEach(input => {
      if (!input.name) return;
      const name = input.name.replace(/-\d+-/, `-${currentForms}-`);
      const id = (input.id || "").replace(/-\d+-/, `-${currentForms}-`);
      input.name = name;
      input.id = id;

      // Limpa valores
      if (input.type !== "hidden") {
        input.value = "";
      }
    });

    container.appendChild(newForm);
    totalForms.value = currentForms + 1;

    aplicarUppercase(newForm); // reaplica caixa alta aos novos inputs

    atualizarNumeracao();
  });

  // Remove serviço
  container.addEventListener("click", (e) => {
    const target = e.target;
    if (target.classList.contains("remove-servico") || target.closest(".remove-servico")) {
      const formRows = container.querySelectorAll(".servico-form");
      if (formRows.length > 1) {
        const toRemove = target.closest(".servico-form");
        if (toRemove) toRemove.remove();
        totalForms.value = parseInt(totalForms.value) - 1;
        atualizarNumeracao();
      } else {
        alert("É necessário ter pelo menos um serviço.");
      }
    }
  });

  atualizarNumeracao();
  aplicarUppercase(container); // aplica caixa alta nos inputs existentes
});

// Lida com o efetivo direto
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-efetivo-direto");
  const leitura = document.getElementById("efetivo-direto-leitura");
  const edicao = document.getElementById("efetivo-direto-edicao");
  const addBtn = document.getElementById("add-efetivo-direto");
  const addBtnContainer = document.getElementById("add-efetivo-direto-container"); // <--- container do botão
  const totalForms = document.querySelector("#id_efetivo_direto-TOTAL_FORMS");

  if (!toggle || !leitura || !edicao || !addBtn || !addBtnContainer || !totalForms) return; // proteção

  // Função para aplicar estado (mostrar/ocultar) com base em `show`
  const setMode = (show) => {
    leitura.style.display = show ? "none" : "block";
    edicao.style.display = show ? "block" : "none";
    // controla o container do botão, não apenas o botão
    addBtnContainer.style.display = show ? "block" : "none";

    // reaplica uppercase nos inputs visíveis (útil quando alterna para edição)
    if (show) {
      aplicarUppercase(edicao);
    }
  };

  // inicializa o estado com base no checkbox (se já estiver checado no HTML)
  setMode(toggle.checked);

  // 🔹 Alterna exibição entre leitura e edição — usa a função setMode
  toggle.addEventListener("change", () => {
    setMode(toggle.checked);
  });

  // 🔹 Atualiza campos "ausente" e "efetivo" dinamicamente
  edicao.addEventListener("input", (e) => {
    const target = e.target;
    if (!target.name) return;
    if (target.name.includes("qtde") || target.name.includes("presente")) {
      const form = target.closest(".efetivo-form");
      if (!form) return;
      const qtdeInput = form.querySelector(`[name*='qtde']`);
      const presenteInput = form.querySelector(`[name*='presente']`);
      const ausente = form.querySelector(".ausente");
      const efetivo = form.querySelector(".efetivo");

      const qtde = Number(qtdeInput ? qtdeInput.value : 0) || 0;
      const presente = Number(presenteInput ? presenteInput.value : 0) || 0;

      if (ausente) ausente.value = Math.max(0, qtde - presente);
      if (efetivo) efetivo.value = presente;
    }
  });

  // 🔹 Adicionar novo formulário
  addBtn.addEventListener("click", () => {
    const currentForms = parseInt(totalForms.value, 10);
    const prototype = edicao.querySelector(".efetivo-form");
    if (!prototype) return;

    const newForm = prototype.cloneNode(true);

    newForm.querySelectorAll("input").forEach(input => {
      if (input.name) {
        input.name = input.name.replace(/-\d+-/, `-${currentForms}-`);
        input.id = (input.id || "").replace(/-\d+-/, `-${currentForms}-`);
      }
      input.value = "";
    });

    edicao.appendChild(newForm);
    totalForms.value = currentForms + 1;

    aplicarUppercase(newForm); // reaplica caixa alta aos novos campos
  });

  // 🔹 Remover formulário
  edicao.addEventListener("click", (e) => {
    const btn = e.target.closest(".remove-efetivo-direto");
    if (btn) {
      const forms = edicao.querySelectorAll(".efetivo-form");
      if (forms.length > 1) {
        const toRemove = btn.closest(".efetivo-form");
        if (toRemove) toRemove.remove();
        totalForms.value = parseInt(totalForms.value, 10) - 1;
      } else {
        alert("Deve haver pelo menos um registro de efetivo direto.");
      }
    }
  });

  // garante uppercase nos inputs já existentes
  aplicarUppercase(edicao);
});


// Lida com o formulário de Efetivo Indireto
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("toggle-efetivo-indireto");
  const leitura = document.getElementById("efetivo-indireto-leitura");
  const edicao = document.getElementById("efetivo-indireto-edicao");
  const addBtnContainer = document.getElementById("add-efetivo-indireto-container");
  const addBtn = document.getElementById("add-efetivo-indireto");
  const totalForms = document.querySelector("#id_efetivo_indireto-TOTAL_FORMS");

  if (!toggle || !leitura || !edicao || !addBtnContainer || !addBtn || !totalForms) return;

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
    const prototype = edicao.querySelector(".efetivo-indireto-form");
    if (!prototype) return;

    const newForm = prototype.cloneNode(true);

    // Atualiza índices e limpa valores
    newForm.querySelectorAll("input, select").forEach(input => {
      if (input.name) {
        input.name = input.name.replace(/-\d+-/, `-${currentForms}-`);
        input.id = (input.id || "").replace(/-\d+-/, `-${currentForms}-`);
      }
      input.value = "";
    });

    edicao.appendChild(newForm);
    totalForms.value = currentForms + 1;

    aplicarUppercase(newForm);
  });

  // 🔹 Pressionar Enter no campo "efetivo" adiciona nova função
  edicao.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && event.target && event.target.name && event.target.name.includes("efetivo")) {
      event.preventDefault(); // Evita envio do formulário
      addBtn.click();         // Simula o clique no botão de adicionar
    }
  });

  // 🔹 Remover formulário
  edicao.addEventListener("click", (e) => {
    const btn = e.target.closest(".remove-efetivo-indireto");
    if (btn) {
      const forms = edicao.querySelectorAll(".efetivo-indireto-form");
      if (forms.length > 1) {
        const toRemove = btn.closest(".efetivo-indireto-form");
        if (toRemove) toRemove.remove();
        totalForms.value = parseInt(totalForms.value) - 1;
      } else {
        alert("Deve haver pelo menos um registro de efetivo indireto.");
      }
    }
  });

  aplicarUppercase(edicao);
});

// lida com as fotos mostrando-as assim que são upadas
document.addEventListener("DOMContentLoaded", () => {
    const inputFotos = document.getElementById('id_fotos');
    const container = document.getElementById('preview');

    if (!inputFotos || !container) return; // proteção caso um dos elementos não exista

    // Função para ajustar horário para fuso de São Paulo (UTC-3)
    const getSaoPauloDateTime = () => {
      const date = new Date();
      const offsetMs = -3 * 60 * 60 * 1000; // UTC-3
      const localDate = new Date(date.getTime() + offsetMs);
      return localDate.toISOString().slice(0,16);
    };

    inputFotos.addEventListener('change', function(event) {
        container.innerHTML = ''; // limpa o preview anterior
        const files = event.target.files;

        Array.from(files).forEach((file, index) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const div = document.createElement('div');
                div.classList.add('col-md-6', 'col-lg-4');
                div.innerHTML = `
                  <div class="card shadow-sm p-2">
                    <img src="${e.target.result}" class="card-img-top rounded" style="height: 180px; object-fit: cover;">
                    <div class="card-body">
                        <input type="text" name="descricao_${index}" class="form-control mb-2" placeholder="Descrição">
                        <input type="datetime-local" name="data_${index}" class="form-control mb-2" value="${getSaoPauloDateTime()}">
                        <button type="button" class="btn btn-sm btn-outline-danger remover-foto w-100"><i class="bi bi-trash"> Remover </i></button>
                    </div>
                  </div>
                `;
                container.appendChild(div);

                aplicarUppercase(div);

                const btn = div.querySelector('.remover-foto');
                if (btn) btn.addEventListener('click', () => div.remove());
            };
            reader.readAsDataURL(file);
        });
    });
});
