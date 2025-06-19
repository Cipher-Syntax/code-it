document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById("comment-input");
    const actions = document.getElementById("comment-actions");
    const cancelBtn = document.getElementById("cancel-btn");

    const imageBtn = document.getElementById("upload-image-btn");
    const gifBtn = document.getElementById("upload-gif-btn");
    const imageInput = document.getElementById("image-upload");
    const gifInput = document.getElementById("gif-upload");

    const previewContainer = document.getElementById("preview-container");

    input.addEventListener("focus", () => {
        input.style.height = "100px";
        actions.style.display = "flex";
    });

    cancelBtn.addEventListener("click", () => {
        input.style.height = "40px";
        input.value = "";
        actions.style.display = "none";
        previewContainer.innerHTML = "";
        previewContainer.style.display = "none";
        imageInput.value = "";
        gifInput.value = "";
    });

    imageBtn.addEventListener("click", () => imageInput.click());
    gifBtn.addEventListener("click", () => gifInput.click());

    imageInput.addEventListener("change", () => handleFilePreview(imageInput.files[0]));
    gifInput.addEventListener("change", () => handleFilePreview(gifInput.files[0]));

    function handleFilePreview(file) {
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            previewContainer.innerHTML = `
                <img src="${e.target.result}" alt="preview" style="width: 60px; height: auto; border-radius: 6px; margin-bottom: 5px;">
            `;
            previewContainer.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    // like
    const commentLike = document.getElementById('comment-likes');

    commentLike.addEventListener('click', function() {
        commentLike.classList.toggle('comment-active');
    });
})