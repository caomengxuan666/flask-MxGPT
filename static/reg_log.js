const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

fistForm.addEventListener("submit", (e) => e.preventDefault());
secondForm.addEventListener("submit", (e) => e.preventDefault());


// 添加两个函数来处理AJAX提交
function submitForm(formId, actionType) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    // 添加actionType到FormData中
    formData.append('action', actionType);

    fetch("/reg_log", {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            form.reset(); // 清空表单
            alert(data.message || "Registration successful."); // 弹出成功提示
            if (actionType === 'login') { // 只有登录成功时才重定向
                window.location.href = "/"; // 或其他您希望登录后跳转的页面
            }
        } else {
            alert(data.message || "An error occurred."); // 弹出错误提示
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was a network issue. Please try again later.");
    });
}


// 修改表单提交事件监听器以使用新函数提交数据
fistForm.addEventListener("submit", (e) => {
    e.preventDefault();
    submitForm("form1", "register");
});

secondForm.addEventListener("submit", (e) => {
    e.preventDefault();
    submitForm("form2", "login");
});