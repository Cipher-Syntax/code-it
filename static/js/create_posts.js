document.addEventListener('DOMContentLoaded', () => {
    const imageBtn = document.getElementById('image');
    const imageInput = document.getElementById("image-upload");
    const imagePreview = document.getElementById('image');
    const feedback = document.getElementById("feedback");


    imageInput.addEventListener('change', () => fileHandler(imageInput.files[0]))
    imageBtn.addEventListener('click', () =>  imageInput.click());


    function fileHandler(file){
        if(!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.innerHTML =   ` <img src="${e.target.result}" alt="preview" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px " > `;

            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
    
    if (feedback) {
        setTimeout(() => {
            feedback.style.display = "block";
        }, 1000);

        setTimeout(() => {
            feedback.style.display = "none";
        }, 2000);
    }


})