// custom.js
function openAvatarUploader() {
    var avatarModal = new bootstrap.Modal(document.getElementById('avatarModal'), {});
    avatarModal.show();
}

function submitAvatar() {
    var form = document.querySelector('#avatarModal form');
    form.submit();
}
