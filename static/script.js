

function previewImage() {
    const file = document.getElementById('image-input').files[0];
    if (!file) {
        document.getElementById('preview').innerHTML = "";
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        const imgElement = document.createElement("img");
        imgElement.src = e.target.result;
        imgElement.style.maxWidth = "500px"; // Set the width of the preview image
        imgElement.style.maxHeight = "500px"; // Set the height of the preview image
        const preview = document.getElementById("preview");
        preview.innerHTML = ""; // Clear previous previews
        preview.appendChild(imgElement);
    };
    reader.readAsDataURL(file);
}

function resetForm() {
    document.getElementById('reset').reset();
    document.getElementById('preview').innerHTML = "";
    document.getElementById('prediction').innerHTML = "";
}

function refreshPage() {
    setTimeout(function() {
        window.location.href = "/";
    }); 
}



// Call the function to start the redirection
window.onload = redirectToHome;