document.addEventListener('DOMContentLoaded', function () {
    const dotMenus = document.querySelectorAll('.dot-menu');

    dotMenus.forEach(menu => {
        menu.addEventListener('click', function (e) {
            e.stopPropagation();
            const selectionBox = menu.nextElementSibling;

            selectionBox.classList.toggle('hidden');
        });
    });

    document.addEventListener('click', function () {
        document.querySelectorAll('.dot-selection').forEach(box => {
            box.classList.add('hidden');
        });
    });
});
