
// Alterna entre login e cadastro //
const areaLogin = document.getElementById('area-login');
const areaCadastro = document.getElementById('area-cadastro');

const btnMostrarCadastro = document.getElementById('btn-mostrar-cadastro');
const btnMostrarLogin = document.getElementById('btn-mostrar-login');

if (btnMostrarCadastro && btnMostrarLogin) {
    btnMostrarCadastro.addEventListener('click', function () {
        areaLogin.style.display = 'none';
        areaCadastro.style.display = 'block';
    });

    btnMostrarLogin.addEventListener('click', function () {
        areaCadastro.style.display = 'none';
        areaLogin.style.display = 'block';
    });
}

// Cadastro do usuário //
const formCadastro = document.getElementById('form-cadastro');

if (formCadastro) {
    formCadastro.addEventListener('submit', async function (evento) {
        evento.preventDefault();

        const usuario = document.getElementById('cadastro-usuario').value.trim();
        const senha = document.getElementById('cadastro-senha').value;

        try {
            const resposta = await requisitarCadastro(usuario, senha);
            const dados = await resposta.json();

            if (resposta.ok) {
                alert('Conta criada com sucesso! Faça login para continuar.');

                document.getElementById('email').value = usuario;
                document.getElementById('senha').value = '';

                formCadastro.reset();
                areaCadastro.style.display = 'none';
                areaLogin.style.display = 'block';
            } else {
                alert('Erro no cadastro: ' +
                    (dados.error || dados.message || 'Tente novamente.'));
            }
        } catch (erro) {
            console.error('Erro ao cadastrar:', erro);
            alert('Erro de conexão ao criar a conta.');
        }
    });
}

// Login do usuário //
const formLogin = document.getElementById('form-login');

if (formLogin) {
    formLogin.addEventListener('submit', async function (evento) {
        evento.preventDefault();

        const usuario = document.getElementById('email').value.trim();
        const senha = document.getElementById('senha').value;

        try {
            const resposta = await requisitarLogin(usuario, senha);
            const dados = await resposta.json();

            if (resposta.ok) {
                tokenJWT = dados.access_token || dados.token;
                localStorage.setItem('equilibra_token', tokenJWT);

                alert('Login realizado com sucesso!');

                mostrarDashboard();
                await carregarDadosPerfil();
            } else {
                alert('Erro no login: ' +
                    (dados.message || dados.error || 'Credenciais inválidas'));
            }
        } catch (erro) {
            console.error('Erro ao realizar login:', erro);
            alert('Erro ao conectar com o servidor Flask.');
        }
    });
}

// Logout do usuário //
const btnSair = document.getElementById('btn-sair');

if (btnSair) {
    btnSair.addEventListener('click', function () {
        localStorage.removeItem('equilibra_token');
        tokenJWT = '';

        const statusPerfil = document.getElementById('status-perfil');
        const resultadoIA = document.getElementById('resultado-ia');

        if (statusPerfil) {
            statusPerfil.textContent = 'Carregando...';
        }

        if (resultadoIA) {
            resultadoIA.textContent = 'Aguardando solicitação...';
        }

        mostrarLogin();

        // Garante que o formulário de login apareça ao sair
        if (areaCadastro && areaLogin) {
            areaCadastro.style.display = 'none';
            areaLogin.style.display = 'block';
        }

        alert('Sessão encerrada com sucesso!');
    });
}
