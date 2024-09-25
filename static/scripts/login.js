$(document).ready(function () {
    // Handle the form submission
    $('form').on('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const username = $('#username').val().trim();
        const password = $('#password').val().trim();

        // Simple client-side validation
        if (!username || !password) {
            $('.error-message').html('<i class="fas fa-exclamation-circle"></i> Both username and password are required.').show();
            return;
        }

        // Clear any previous error messages
        $('.error-message').hide();

        // AJAX request to login the user
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            contentType: 'application/json',
            data: JSON.stringify({ username: username, password: password }),
            success: function (response) {
                // Retrieve the redirect URL from the query parameters
                const urlParams = new URLSearchParams(window.location.search);
                const redirectUrl = urlParams.get('redirectUrl') || sessionStorage.getItem('redirectUrl');
                // const redirectUrl = sessionStorage.getItem('redirectUrl');
                
                // Redirect to the previous page or fallback to /home
                if (redirectUrl) {
                    sessionStorage.removeItem('redirectUrl'); // Clear the URL after redirect
                    window.location.href = decodeURIComponent(redirectUrl);
                } else {
                    window.location.href = '/home';
                }
            },
            error: function (xhr) {
                // Display the error message
                console.log('Error: ', xhr.responseJSON.message);
                const errorMsg = xhr.responseJSON.message ? xhr.responseJSON.message : 'An error occurred. Please try again.';
                
                $('.error-message').html('<i class="fas fa-exclamation-circle"></i> ' + errorMsg).show();
            }
        });
    });

    // Toggle password visibility
    $('#show-confirm-password').on('change', function () {
        const passwordField = $('#password');
        if ($(this).is(':checked')) {
            passwordField.attr('type', 'text');
        } else {
            passwordField.attr('type', 'password');
        }
    });

    // Append redirectUrl to the signup link if available
    let redirectUrl = sessionStorage.getItem('redirectUrl');
    const signupLink = $('.signup-link a');
    if (redirectUrl) {
        // Append the redirect URL as a query parameter to the signup link
        signupLink.attr('href', signupLink.attr('href') + '?redirectUrl=' + encodeURIComponent(redirectUrl));
    } else {
        let redirectUrl = sessionStorage.setItem('redirectUrl');

        signupLink.attr('href', signupLink.attr('href') + '?redirectUrl=' + encodeURIComponent(redirectUrl));
    }
});

