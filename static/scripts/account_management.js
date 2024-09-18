$(document).ready(function () {
    // Configure Toastr options
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-center",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    // Example function to show a success message
    // Function to show success toast with optional delay for reload/redirect
    function showSuccess(message, callback = null) {
        toastr.success(message);

        // If a callback is provided (like a redirect or reload), execute it after 2 seconds
        if (callback) {
            setTimeout(callback, 3000); // Adjust the delay as needed
        }
    }

    // Example function to show an error message
    function showError(message) {
        toastr.error(message);
    }

    // Toggle password visibility
    $('.toggle-password').on('click', function () {
        const passwordField = $('#password');
        const passwordFieldType = passwordField.attr('type');

        if (passwordFieldType === 'password') {
            passwordField.attr('type', 'text');
            $(this).removeClass('fa-eye').addClass('fa-eye-slash'); // Change the icon
        } else {
            passwordField.attr('type', 'password');
            $(this).removeClass('fa-eye-slash').addClass('fa-eye'); // Change the icon back
        }
    });

    const initialUsername = $('#username').val();
    const initialEmail = $('#email').val();
    const initialFirstName = $('#first_name').val();
    const initialLastName = $('#last_name').val();
    const initialPhoneNumber = $('#phone_number').val();
    const userId = $('#user-id').val();

    // Handle update profile form submission
    $('#update-profile-form').submit(function (event) {
        event.preventDefault(); // Prevent traditional form submission

        let username = $('#username').val();
        let email = $('#email').val();
        let password = $('#password').val();
        let firstName = $('#first_name').val();
        let lastName = $('#last_name').val();
        let phoneNumber = $('#phone_number').val();

        // Client-side validation for email format
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            showError('Please enter a valid email address.');
            return;
        }

        // Prepare data for the update request
        let data = {};

        console.log("initial:", username);
        // Include only changed fields in the update request
        if (username !== initialUsername) {
            data.username = username;
            console.log("Username:", data.username);
            
        }
        if (email !== initialEmail) {
            data.email = email;
        }
        if (firstName !== initialFirstName) {
            data.first_name = firstName;
        }
        if (lastName !== initialLastName) {
            data.last_name = lastName;
        }
        if (phoneNumber !== initialPhoneNumber) {
            data.phone_number = phoneNumber;
        }

        // Include password only if it is set
        if (password) {
            data.password = password;
        }

        // If no data was modified, show a message
        if ($.isEmptyObject(data)) {
            showError('No changes were made.');
            return;
        }

        // Make the AJAX call to update the user profile
        $.ajax({
            url: `/api/v1/users/${userId}`, // Update this endpoint to match your API route
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                // Show success message and reload after 2 seconds
                showSuccess('Profile updated successfully.', function() {
                    window.location.reload();
                });
            },
            error: function (xhr) {
                let errorMsg = xhr.responseJSON.message || 'An error occurred. Please try again.';
                showError(errorMsg);
            }
        });
    });

    // Handle delete profile action
    $('.delete-button').on('click', function (event) {
        event.preventDefault(); // Prevent traditional form submission

        if (!confirm("Are you sure you want to delete your profile? This action cannot be undone.")) {
            return; // Exit if user cancels the action
        }

        // Make the AJAX call to delete the user profile
        $.ajax({
            url: `/api/v1/users/${userId}`, // Update this endpoint to match your API route
            method: 'DELETE',
            success: function (response) {
                // Show success message and delay redirect
                showSuccess('Profile deleted successfully.', function() {
                    console.log("Redirecting to home page...");
                    window.location.href = '/home'; // Redirect to home page after 9 seconds
                });
            },
            error: function (xhr) {
                let errorMsg = xhr.responseJSON.message || 'An error occurred. Please try again.';
                showError(errorMsg);
            }
        });
    });
});
