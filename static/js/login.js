document.addEventListener('DOMContentLoaded', function () {
    const senhaInput = document.getElementById('senha');
    const eyeIcon = document.querySelector('.fa-eye');
    
    // Verifica se o ícone foi clicado
    eyeIcon.addEventListener('click', function () {
        // Alterna entre mostrar e esconder a senha
        if (senhaInput.type === 'password') {
            senhaInput.type = 'text';
            eyeIcon.classList.add('fa-eye-slash');
            eyeIcon.classList.remove('fa-eye');
        } else {
            senhaInput.type = 'password';
            eyeIcon.classList.add('fa-eye');
            eyeIcon.classList.remove('fa-eye-slash');
        }
    });
});
