// Função que aplica o uppercase em todos os inputs de texto
function aplicarUppercase(container = document) {
  container.querySelectorAll("input[type='text']").forEach(input => {
    // Evita duplicar listeners
    input.removeEventListener("input", input._upperListener);
    input._upperListener = () => { input.value = input.value.toUpperCase(); };
    input.addEventListener("input", input._upperListener);
  });
}

// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  aplicarUppercase();
});

//Formata todos os campos que tenham tel no id com expressões regulares
//adicionando os caracteres de separação no telefone (xx) xxxxx-xxxx
document.addEventListener('DOMContentLoaded', function () {
    var telefoneInputs = document.querySelectorAll('[id*="tel"], [name*="tel"]');

    telefoneInputs.forEach(function (telefoneInput) {
        telefoneInput.addEventListener('input', function (event) {
            var telefone = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos

            if (telefone.length >= 8) {
                if (telefone.length === 11) {
                    this.value = telefone.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
                } else {
                    this.value = telefone.replace(/^(\d{2})(\d{4,5})(\d{4})/, '($1) $2-$3');
                }
            } else {
                this.value = telefone.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
            }
        });
    });
});

//Formata o campo data com expressões regulares
//adicionando a barra / para separar a data no formato padrão xx/xx/xxxx
document.addEventListener('DOMContentLoaded', function () {
    var dataInputs = document.querySelectorAll('[id*="data"]');

    dataInputs.forEach(function (input) {
        input.addEventListener('input', formatarData);
    });

    function formatarData(event) {
        var data = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos

        if (data.length === 8) {
            this.value = data.replace(/^(\d{2})(\d{2})(\d{4})$/, '$1/$2/$3');
        } else {
            this.value = data.replace(/^(\d{2})(\d{0,2})(\d{0,4})$/, '$1/$2/$3');
        }
    }
});


//Formata o campo id_cep com expressões regulares
//adicionando o '.' e o '-' xx.xxx-xxx
document.addEventListener('DOMContentLoaded', function () {
    var cepInput = document.getElementById('id_cep');
    if (cepInput) {
        cepInput.addEventListener('input', function (event) {
            var cep = this.value.replace(/\D/g, ''); // Remove caracteres não numéricos

            if (cep.length === 8) {
                this.value = cep.replace(/^(\d{5})(\d{3})$/, '$1-$2');
            } else {
                this.value = cep.replace(/^(\d{5})(\d{0,3})$/, '$1-$2');
            }
        });
    }
});

//Valida se o cnpj digitado é verdadeiro, não consulta os dados externamente
//Após validação faz a formatação usando expressões regulares no formato xx.xxx.xxx/xxxx-xx
document.addEventListener('DOMContentLoaded', function () {
    // Verifique se o campo CNPJ está presente na página
    var cnpjInput = document.getElementById('id_cnpj');
    if (cnpjInput) {
        // Adicione um ouvinte de eventos para formatar o CNPJ enquanto o usuário digita
        cnpjInput.addEventListener('input', function () {
            // Obtenha o valor do CNPJ digitado pelo usuário
            var cnpj = cnpjInput.value;
            // Remova qualquer formatação existente do CNPJ
            var cnpjLimpo = cnpj.replace(/\D/g, '');

            // Verifique se o CNPJ tem um tamanho válido e formate-o
            if (cnpjLimpo.length === 14) {
                var cnpjFormatado = formatarCnpj(cnpjLimpo);
                // Defina o valor formatado no campo de entrada
                cnpjInput.value = cnpjFormatado;
            }
        });
    }

    // Função para formatar CNPJ
    function formatarCnpj(cnpj) {
        return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
    }
});

//Muda o tipo do input do password entre 'text' e 'password'
//Tem que inserir um checkbox em todo formulario que esses campos aparecem com o nome showPassword
//Para que o código abaixo funcione
document.addEventListener('DOMContentLoaded', function () {
    var showPasswordCheckbox = document.getElementById('showPassword');

    if (showPasswordCheckbox) {
        showPasswordCheckbox.addEventListener('change', function () {
            var password1Input = document.getElementById('id_password1');
            var password2Input = document.getElementById('id_password2');
            var newPassword1Input = document.getElementById('id_new_password1');
            var newPassword2Input = document.getElementById('id_new_password2');

            if (password1Input && password2Input) {
                var type = this.checked ? 'text' : 'password';
                password1Input.setAttribute('type', type);
                password2Input.setAttribute('type', type);
            }

            if (newPassword1Input && newPassword2Input) {
                var type = this.checked ? 'text' : 'password';
                newPassword1Input.setAttribute('type', type);
                newPassword2Input.setAttribute('type', type);
            }
        });
    }
});

