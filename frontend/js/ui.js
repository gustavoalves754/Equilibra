// Exibe a tela do Dashboard e oculta o Login
function mostrarDashboard() {
    const secaoLogin = document.getElementById('secao-login');
    const secaoDashboard = document.getElementById('secao-dashboard');

    if (secaoLogin) secaoLogin.style.display = 'none';
    if (secaoDashboard) secaoDashboard.style.display = 'block';
}

// Exibe a tela de Login e oculta o Dashboard
function mostrarLogin() {
    const secaoLogin = document.getElementById('secao-login');
    const secaoDashboard = document.getElementById('secao-dashboard');

    if (secaoLogin) secaoLogin.style.display = 'block';
    if (secaoDashboard) secaoDashboard.style.display = 'none';
}

// Atualiza o texto do perfil na tela
function atualizarTextoPerfil(texto) {
    const statusPerfil = document.getElementById('status-perfil');
    if (statusPerfil) statusPerfil.textContent = texto;
}

// Atualiza a mensagem da resposta da IA

function atualizarTextoIA(texto) {
    const resultadoIA = document.getElementById('resultado-ia');

    if (!resultadoIA) return;

    // Limpa o conteúdo anterior.
    resultadoIA.replaceChildren();

    // Divide o Markdown em linhas.
    const linhas = String(texto || '').split('\n');
    let listaAtual = null;

    function adicionarTextoFormatado(elemento, conteudo) {
        // Converte **negrito** sem interpretar HTML.
        const partes = conteudo.split(/(\*\*.*?\*\*)/g);

        partes.forEach(parte => {
            if (parte.startsWith('**') && parte.endsWith('**')) {
                const negrito = document.createElement('strong');
                negrito.textContent = parte.slice(2, -2);
                elemento.appendChild(negrito);
            } else if (parte) {
                elemento.appendChild(document.createTextNode(parte));
            }
        });
    }

    linhas.forEach(linha => {
        const textoLinha = linha.trim();

        // Ignora linhas vazias e separadores Markdown.
        if (!textoLinha || /^---+$/.test(textoLinha)) {
            listaAtual = null;
            return;
        }

        // Converte títulos Markdown.
        const titulo = textoLinha.match(/^(#{1,3})\s+(.+)$/);

        if (titulo) {
            listaAtual = null;

            const h3 = document.createElement('h3');
            adicionarTextoFormatado(h3, titulo[2]);
            resultadoIA.appendChild(h3);
            return;
        }

        // Converte itens de lista.
        const itemLista = textoLinha.match(/^[-*]\s+(.+)$/);

        if (itemLista) {
            if (!listaAtual) {
                listaAtual = document.createElement('ul');
                resultadoIA.appendChild(listaAtual);
            }

            const item = document.createElement('li');
            adicionarTextoFormatado(item, itemLista[1]);
            listaAtual.appendChild(item);
            return;
        }

        // Converte parágrafos.
        listaAtual = null;

        const paragrafo = document.createElement('p');
        adicionarTextoFormatado(paragrafo, textoLinha);
        resultadoIA.appendChild(paragrafo);
    });
}
