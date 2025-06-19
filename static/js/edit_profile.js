document.addEventListener('DOMContentLoaded', () => {
    const bio = document.getElementById('profile-bio');
    const image = document.getElementById('profile-image-img'); // Fix here
    const imageUpload = document.getElementById("image-upload");
    const saveBtn = document.getElementById('save-btn');

    image.addEventListener('click', () => {
        saveBtn.style.display = "block";
        if (imageUpload) {
            imageUpload.click();
        }
    });

    imageUpload.addEventListener("change", function () {
        const file = this.files[0];
        if (file && image) {
            const reader = new FileReader();
            reader.onload = function (e) {
                image.src = e.target.result;
            }
            reader.readAsDataURL(file);
        }
    });

    bio.addEventListener('focus', () => {
        saveBtn.style.display = 'block';
    });

    // document.addEventListener('click', (event) => {
    //     if (event.target !== bio && event.target !== image) {
    //         saveBtn.style.display = 'none';
    //     }
    // });
});
