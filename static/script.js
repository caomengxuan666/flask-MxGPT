document.addEventListener('DOMContentLoaded', (event) => {
    const inputImageWrapper = document.getElementById('inputImageWrapper');
    const outputImageWrapper = document.getElementById('outputImageWrapper');
    inputImageWrapper.classList.add('no-image');
    outputImageWrapper.classList.add('no-image');
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const inputImage = document.getElementById('inputImage');
            inputImage.src = e.target.result;
            inputImage.style.display = 'block';
            const inputImageWrapper = inputImage.parentElement;
            inputImageWrapper.classList.remove('no-image');
            inputImageWrapper.classList.add('has-image');
        };
        reader.readAsDataURL(file);
    }
});

document.querySelector('.file-label').addEventListener('click', function() {
    event.preventDefault(); // 取消点击事件的默认行为
    document.getElementById('fileInput').click();
});

document.getElementById('segmentButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('image', file);

        fetch('/segment', {
            method: 'POST',
            body: formData
        })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const outputImage = document.getElementById('outputImage');
                outputImage.src = url;
                outputImage.style.display = 'block';
                const outputImageWrapper = outputImage.parentElement;
                outputImageWrapper.classList.remove('no-image');
                outputImageWrapper.classList.add('has-image');
            })
            .catch(error => console.error('Error:', error));
    } else {
        alert('Please upload an image first.');
    }
});
