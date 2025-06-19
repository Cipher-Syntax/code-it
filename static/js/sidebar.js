document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');

    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
    });

    // like
    const like = document.getElementById('likes');

    like.addEventListener('click', function() {
        like.classList.toggle('active');
    });
})