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

document.querySelector('.file-label').addEventListener('click', function(event) {
    event.preventDefault(); // 取消点击事件的默认行为
    document.getElementById('fileInput').click();
});

document.getElementById('segmentButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        showProgressBar(); // 显示进度条

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('image', file);

        fetch('/DR_enhance', {
            method: 'POST',
            body: formData
        })
            .then(response => response.blob())
            .then(blob => {
                hideProgressBar(); // 隐藏进度条

                const url = URL.createObjectURL(blob);
                const outputImage = document.getElementById('outputImage');
                outputImage.src = url;
                outputImage.style.display = 'block';
                const outputImageWrapper = outputImage.parentElement;
                outputImageWrapper.classList.remove('no-image');
                outputImageWrapper.classList.add('has-image');
            })
            .catch(error => {
                hideProgressBar(); // 如果有错误也隐藏进度条
                console.error('Error:', error);
            });
    } else {
        alert('Please upload an image first.');
    }
});

function showProgressBar() {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.display = 'block';
    simulateProgress(); // 开始模拟进度
}

function hideProgressBar() {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.display = 'none';
}

// 模拟进度条填充的函数
function simulateProgress() {
    let width = 0;
    const progressBarFill = document.getElementById('progressBarFill');
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width += 3; // 增加宽度，这里可以根据需要调整速度
            progressBarFill.style.width = width + '%';
        }
    }, 100); // 每100毫秒检查一次
}
