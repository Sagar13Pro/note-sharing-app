$(document).ready(function () {

    //MARK: - Show/Hide => Password
    let passwd = $('#passwd');
    $('#eye-pass').on("click", function () {
        if (passwd.val().length > 0) {
            if (passwd.attr('type') === 'password') {
                $(this).attr('class', 'fas fa-eye');
                passwd.attr('type', 'text');
            } else {
                $(this).attr('class', 'fas fa-eye-slash');
                passwd.attr('type', 'password');
            }
        } else {
            if ($('.passwd-error').length === 0) {
                passwd.after('<div class="passwd-error" style="color:#f00;transition: 0.3s ease-in;font-weight:600;margin: 0 0 0.3em 0.3em">Provide Input First</div>');
            } else {
                $('.passwd-error').remove();
            }
        }
    });
    //MARK: - Show/Hide passsword =>  for confirmation
    let passwd_confirm = $('#passwd-confirm');
    $('#eye-cpass').on("click", function () {
        if (passwd_confirm.val().length > 0) {
            if (passwd_confirm.attr('type') === 'password') {
                $(this).attr('class', 'fas fa-eye');
                passwd_confirm.attr('type', 'text');
            } else {
                $(this).attr('class', 'fas fa-eye-slash');
                passwd_confirm.attr('type', 'password');
            }
        } else {
            if ($('.passwd-confirm-error').length === 0) {
                passwd_confirm.after('<div class="passwd-confirm-error" style="color:#f00;transition: 0.3s ease-in;font-weight:600;margin: 0 0 0.3em 0.3em">Provide Input First</div>');
            } else {
                $('.passwd-confirm-error').remove();
            }
        }
    });

    //MARK: - Password validation 
    //OnFocus show 
    passwd.on("focus", function () {
        console.log('ok')
    });
});