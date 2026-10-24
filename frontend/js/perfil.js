// Carrega os dados do perfil //
async function carregarDadosPerfil() {
    try {
        const resposta = await requisitarPerfil(tokenJWT);

        if (!resposta.ok) {
            atualizarTextoPerfil(
                'Perfil não configurado. Preencha os dados acima!'
            );
            return;
        }

        const perfil = await resposta.json();

        // Aceita os nomes dos campos usados pelo backend
        const idade = perfil.age ?? perfil.idade ?? '';
        const peso = perfil.weight_kg ?? perfil.peso ?? '';
        const altura = perfil.height_m ?? perfil.altura ?? '';
        const objetivo = perfil.goal ?? perfil.objetivo ?? '';

        // Preenche o formulário com os dados salvos
        document.getElementById('idade').value = idade;
        document.getElementById('peso').value = peso;
        document.getElementById('altura').value = altura;
        document.getElementById('objetivo').value = objetivo;

        atualizarTextoPerfil(
            `Idade: ${idade !== '' ? idade : 'N/A'} | ` +
            `Peso: ${peso !== '' ? peso : 'N/A'}kg | ` +
            `Altura: ${altura !== '' ? altura : 'N/A'}m`
        );
    } catch (erro) {
        console.error('Erro ao carregar perfil:', erro);
        atualizarTextoPerfil('Erro ao carregar dados do perfil.');
    }
}

// Salva as alterações do perfil //
const formPerfil = document.getElementById('form-perfil');

if (formPerfil) {
    formPerfil.addEventListener('submit', async function (evento) {
        evento.preventDefault();

        const idadeTexto = document.getElementById('idade').value.trim();
        const pesoTexto = document.getElementById('peso').value.trim();
        const alturaTexto = document.getElementById('altura').value.trim();
        const objetivo = document.getElementById('objetivo').value.trim();

        const idade = Number(idadeTexto);
        const peso = Number(pesoTexto.replace(',', '.'));
        const altura = Number(alturaTexto.replace(',', '.'));

        // Confere se todos os campos foram preenchidos corretamente
        if (
            idadeTexto === '' ||
            pesoTexto === '' ||
            alturaTexto === '' ||
            !Number.isInteger(idade) ||
            idade <= 0 ||
            !Number.isFinite(peso) ||
            peso <= 0 ||
            !Number.isFinite(altura) ||
            altura <= 0 ||
            objetivo === ''
        ) {
            alert('Preencha todos os campos com valores válidos.');
            return;
        }

        const dadosPerfil = {
            age: idade,
            weight_kg: peso,
            height_m: altura,
            goal: objetivo
        };

        try {
            const resposta = await requisitarSalvarPerfil(
                tokenJWT,
                dadosPerfil
            );

            const dados = await resposta.json();

            if (resposta.ok) {
                alert('Perfil atualizado com sucesso!');
                await carregarDadosPerfil();
            } else {
                alert(
                    'Erro ao salvar perfil: ' +
                    (dados.message || dados.error || 'Tente novamente.')
                );
            }
        } catch (erro) {
            console.error('Erro ao salvar perfil:', erro);
            alert('Erro de conexão ao salvar perfil.');
        }
    });
}