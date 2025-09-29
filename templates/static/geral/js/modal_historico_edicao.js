<script>
document.addEventListener("DOMContentLoaded", function () {
    const modalElement = document.getElementById("historicoModal");

    // Verifica se o modal existe antes de adicionar o listener
    if (modalElement) {
        modalElement.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;

            if (!button) return;

            const tipo = button.getAttribute("data-tipo");
            const id = button.getAttribute("data-id");

            const lista = document.getElementById("lista-historico");
            if (!lista) return;

            lista.innerHTML = "<li class='list-group-item'>Carregando...</li>";

            fetch(`/historico/${tipo}/${id}/`)
                .then(response => {
                    if (!response.ok) throw new Error("Erro ao carregar histórico");
                    return response.json();
                })
                .then(dados => {
                    lista.innerHTML = "";
                    if (dados.length === 0) {
                        lista.innerHTML = "<li class='list-group-item'>Nenhuma edição registrada.</li>";
                    } else {
                        dados.forEach(item => {
                            const li = document.createElement("li");
                            li.className = "list-group-item";
                            li.innerHTML = `<strong>${item.usuario}</strong> (${item.data}): <br>${item.descricao}`;
                            lista.appendChild(li);
                        });
                    }
                })
                .catch(error => {
                    lista.innerHTML = `<li class='list-group-item text-danger'>Erro ao carregar histórico.</li>`;
                    console.error(error);
                });
        });
    }
});
</script>
