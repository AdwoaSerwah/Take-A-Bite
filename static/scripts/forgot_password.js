$(document).ready(function () {
    $('#forgot-password-form').on('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Gather form data
        const email = $('#email').val();

        // Send the data via AJAX
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            contentType: 'application/json',
            data: JSON.stringify({ email: email }),
            success: function (response) {
                // Handle successful response
                // alert(response);
                window.location.href = '/check_email'; // Redirect to login page or specified URL
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
