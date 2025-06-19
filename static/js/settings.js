document.addEventListener('DOMContentLoaded', () => {
    const editFormSection = [
        { editSection: 'firstname-section', forms: 'edit-firstname' },
        { editSection: 'lastname-section', forms: 'edit-lastname' },
        { editSection: 'email-section', forms: 'edit-email' },
        { editSection: 'bio-section', forms: 'edit-bio' }
    ];

    editFormSection.forEach(({ editSection, forms }) => {
        const button = document.getElementById(editSection);
        const form = document.getElementById(forms);

        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            form.style.display = 'flex';
        });

        form.addEventListener('click', (e) => {
            e.stopPropagation();
        });

        document.addEventListener('click', (e) => {
            if (!form.contains(e.target) && e.target !== button) {
                form.style.display = 'none';
            }
        });
    });
});
