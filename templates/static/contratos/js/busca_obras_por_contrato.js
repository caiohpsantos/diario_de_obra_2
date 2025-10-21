document.addEventListener("DOMContentLoaded", () => {
  const contratoSelect = document.getElementById("contratoSelect");
  const obraSelect = document.getElementById("obraSelect");

  contratoSelect.addEventListener("change", () => {
    const contratoId = contratoSelect.value;

    // limpa as opções anteriores
    obraSelect.innerHTML = "<option value=''>-- Selecione a obra --</option>";

    if (contratoId) {
      fetch(`/contratos/obras_por_contrato/${contratoId}/`)
        .then(response => {
          if (!response.ok) throw new Error(`Erro HTTP ${response.status}`);
          return response.json();
        })

        .then(data => {
          data.forEach(obra => {
            const opt = document.createElement("option");
            opt.value = obra.id;
            opt.textContent = obra.nome;
            obraSelect.appendChild(opt);
          });
        })
        .catch(err => {
          console.error("Erro ao carregar obras:", err);
          alert("Não foi possível carregar as obras do contrato selecionado.");
        });
    }
  });
});