// Token usado para manter a sessão do usuário
let tokenJWT = localStorage.getItem('equilibra_token') || '';

// Abre a tela correta ao carregar a página
if (tokenJWT) {
    mostrarDashboard();
    carregarDadosPerfil();
} else {
    mostrarLogin();
}