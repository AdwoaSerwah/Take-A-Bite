$(document).ready(function() {
    // Toggle password visibility
    $('#show-password').change(function() {
        let passwordField = $('#password');
        passwordField.attr('type', this.checked ? 'text' : 'password');
    });

    $('#show-confirm-password').change(function() {
        let confirmPasswordField = $('#confirm-password');
        confirmPasswordField.attr('type', this.checked ? 'text' : 'password');
    });

    // Handle signup form submission
    $('#signup-form').submit(function(event) {
        event.preventDefault(); // Prevent traditional form submission

        let firstName = $('#first_name').val();
        let lastName = $('#last_name').val();
        let username = $('#username').val();
        let email = $('#email').val();
        let phoneNumber = $('#phone_number').val(); // Match the ID in HTML
        let password = $('#password').val();
        let confirmPassword = $('#confirm-password').val();
        let errorMessage = $('#error-message');

        // Regular expression for validating email format
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Client-side validation
        if (password !== confirmPassword) {
            errorMessage.text('Passwords do not match!').show();
            return;
        }

        if (!emailPattern.test(email)) {
            errorMessage.text('Please enter a valid email address.').show();
            return;
        }

        errorMessage.hide(); // Clear any previous errors

        // Make the API call for signup
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                username: username,
                email: email,
                phone_number: phoneNumber,
                password: password
            }),
            success: function (response) {
                // Retrieve the redirect URL from the query parameters
                const urlParams = new URLSearchParams(window.location.search);
                const redirectUrl = urlParams.get('redirectUrl') || sessionStorage.getItem('redirectUrl');
                
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

    // Append redirectUrl to the login link if available
    let redirectUrl = sessionStorage.getItem('redirectUrl');
    const loginLink = $('.login-link a');
    if (redirectUrl) {
        // Append the redirect URL as a query parameter to the login link
        loginLink.attr('href', loginLink.attr('href') + '?redirectUrl=' + encodeURIComponent(redirectUrl));
    } else {
        let redirectUrl = sessionStorage.setItem('redirectUrl');

        loginLink.attr('href', loginLink.attr('href') + '?redirectUrl=' + encodeURIComponent(redirectUrl));
    }
});














/*$(document).ready(function() {
    // Toggle password visibility
    $('#show-password').change(function() {
        let passwordField = $('#password');
        passwordField.attr('type', this.checked ? 'text' : 'password');
    });

    $('#show-confirm-password').change(function() {
        let confirmPasswordField = $('#confirm-password');
        confirmPasswordField.attr('type', this.checked ? 'text' : 'password');
    });

    // Handle signup form submission
    $('#signup-form').submit(function(event) {
        event.preventDefault(); // Prevent traditional form submission

        let firstName = $('#first_name').val();
        let lastName = $('#last_name').val();
        let username = $('#username').val();
        let email = $('#email').val();
        let phoneNumber = $('#phone_number').val(); // Match the ID in HTML
        let password = $('#password').val();
        let confirmPassword = $('#confirm-password').val();
        let errorMessage = $('#error-message');

        // Regular expression for validating email format
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Client-side validation
        if (password !== confirmPassword) {
            errorMessage.text('Passwords do not match!').show();
            return;
        }

        if (!emailPattern.test(email)) {
            errorMessage.text('Please enter a valid email address.').show();
            return;
        }

        errorMessage.hide(); // Clear any previous errors

        // Make the API call for signup
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                username: username,
                email: email,
                phone_number: phoneNumber,
                password: password
            }),
            success: function (response) {
                // Retrieve the previous page URL from sessionStorage
                // const previousPage = sessionStorage.getItem('previousPage');
                const redirectUrl = sessionStorage.getItem('redirectUrl');
                console.log(redirectUrl)
                
                // Redirect to the previous page or fallback to /home
                if (redirectUrl) {
                    // window.location.href = previousPage;
                    sessionStorage.removeItem('redirectUrl');
                    window.location.href = decodeURIComponent(redirectUrl);
                } else {
                    window.location.href = '/home';
                }
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
});*/











/*$(document).ready(function() {
    // Toggle password visibility
    $('#show-password').change(function() {
        let passwordField = $('#password');
        passwordField.attr('type', this.checked ? 'text' : 'password');
    });

    $('#show-confirm-password').change(function() {
        let confirmPasswordField = $('#confirm-password');
        confirmPasswordField.attr('type', this.checked ? 'text' : 'password');
    });

    // Handle signup form submission
    $('#signup-form').submit(function(event) {
        event.preventDefault(); // Prevent traditional form submission

        let firstName = $('#first_name').val();
        let lastName = $('#last_name').val();
        let username = $('#username').val();
        let email = $('#email').val();
        let phoneNumber = $('#phone_number').val(); // Match the ID in HTML
        let password = $('#password').val();
        let confirmPassword = $('#confirm-password').val();
        let errorMessage = $('#error-message');

        // Regular expression for validating email format
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        // Client-side validation
        if (password !== confirmPassword) {
            errorMessage.text('Passwords do not match!').show();
            return;
        }

        if (!emailPattern.test(email)) {
            errorMessage.text('Please enter a valid email address.').show();
            return;
        }

        errorMessage.hide(); // Clear any previous errors

        // Make the API call for signup
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                username: username,
                email: email,
                phone_number: phoneNumber,
                password: password
            }),
            success: function (response) {
                // Retrieve the previous page URL from sessionStorage
                const previousPage = sessionStorage.getItem('previousPage');
                console.log(previousPage)
                
                // Redirect to the previous page or fallback to /home
                if (previousPage) {
                    window.location.href = previousPage;
                } else {
                    window.location.href = '/home';
                }
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
})*/
