$(document).ready(function() {
    // Toggle password visibility
    $('.toggle-password').on('click', function() {
        const passwordField = $(this).siblings('input');
        const passwordFieldType = passwordField.attr('type') === 'password' ? 'text' : 'password';
        passwordField.attr('type', passwordFieldType);
        
        // Toggle the eye icon
        const icon = $(this).find('i');
        if (passwordFieldType === 'password') {
            icon.removeClass('fa-eye-slash').addClass('fa-eye');
        } else {
            icon.removeClass('fa-eye').addClass('fa-eye-slash');
        }
    });

    // Reset password
    $('#reset-password-form').on('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        const new_password = $('#password').val();
        const confirmPassword = $('#confirm-password').val();

        // Simple client-side validation
        if (new_password !== confirmPassword) {
            $('#message').text('Passwords do not match.');
            return;
        }

        // Prepare data to be sent in the POST request
        let data = {
            new_password: new_password
        };
        console.log(data)

        $.ajax({
            url: $(this).attr('action'), // URL from the form's action attribute
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                $('#message').text(response.message || 'Password reset successfully.');
                window.location.href = '/login';
                // You might want to redirect the user or perform another action on success
            },
            error: function (xhr) {
                // Display the error message
                console.log('Error: ', xhr.responseJSON.message)
                const errorMsg = xhr.responseJSON.message ? xhr.responseJSON.message : 'An error occurred. Please try again.';
 
                // $('.error-message').text(errorMsg).show();
                $('.error-message').html('<i class="fas fa-exclamation-circle"></i> ' + errorMsg).show();
            }
        });
    });
});
