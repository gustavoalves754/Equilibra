// Gera uma orientação usando a IA
const btnGerarIA = document.getElementById('btn-gerar-ia');

if (btnGerarIA) {
    btnGerarIA.addEventListener('click', async function () {
        atualizarTextoIA('Aguarde a sugestão...');

        try {
            const resposta = await requisitarOrientacaoIA(tokenJWT);
            const dados = await resposta.json();

            if (!resposta.ok) {
                atualizarTextoIA(
                    'Erro ao gerar orientação: ' +
                    (dados.error || dados.message || 'Tente novamente.')
                );
                return;
            }

            // Verifica em qual campo o backend retornou a resposta
            const textoIA =
                dados.orientacao ||
                dados.conteudo ||
                dados.guidance ||
                dados.message ||
                dados.response ||
                (typeof dados === 'string' ? dados : '');

            atualizarTextoIA(
                textoIA || 'A IA não retornou uma orientação válida.'
            );
        } catch (erro) {
            console.error('Erro ao consultar a IA:', erro);
            atualizarTextoIA('Erro de conexão ao chamar a IA.');
        }
    });
}