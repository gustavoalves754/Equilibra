// 1. Cadastrar um novo usuário
async function requisitarCadastro(usuario, senha) {
    const resposta = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: usuario,
            password: senha
        })
    });

    return resposta;
}

// 2. Autenticação (Login)
async function requisitarLogin(email, senha) {
    const resposta = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            usuario: email,
            username: email,
            email: email,
            senha: senha,
            password: senha
        })
    });

    return resposta;
}

// 3. Buscar dados do perfil
async function requisitarPerfil(token) {
    const resposta = await fetch('/api/v1/profile', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    });

    return resposta;
}

// 4. Gerar orientação com IA
async function requisitarOrientacaoIA(token) {
    const resposta = await fetch('/api/v1/guidance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({})
    });

    return resposta;
}

// 5. Salvar ou atualizar o perfil
async function requisitarSalvarPerfil(token, dadosPerfil) {
    const resposta = await fetch('/api/v1/profile', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify(dadosPerfil)
    });

    return resposta;
}