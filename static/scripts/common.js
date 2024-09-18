$(document).ready(function () {
    sessionStorage.setItem('redirectUrl', encodeURIComponent(window.location.href));

    let redirectUrl = sessionStorage.getItem('redirectUrl');

    if (redirectUrl) {
        const signupLink = $('.signup-link a');
        const loginLink = $('.login-link a');

        // Append the redirectUrl to the href attributes of the signup and login links
        signupLink.attr('href', function (i, href) {
            return href + '?redirectUrl=' + redirectUrl;
        });
        loginLink.attr('href', function (i, href) {
            return href + '?redirectUrl=' + redirectUrl;
        });
    }
    
    // Toggle the main menu
    $('#menu-icon').click(function () {
        $('.nav-links').toggleClass('active');
        $(this).toggleClass('active');
    });

    // Toggle user profile dropdown
    $('.dropdown-toggle').click(function (event) {
        event.stopPropagation(); // Prevent click from bubbling up to the document
        $(this).next('.dropdown-content').toggleClass('active');
        $(this).toggleClass('active');
    });

    // Toggle settings nested dropdown
    $('.nested-dropdown-toggle').click(function (event) {
        event.stopPropagation(); // Prevent click from bubbling up to the document
        $(this).next('.nested-dropdown-content').toggleClass('active');
        $(this).toggleClass('active');
    });

    // Hide dropdowns when clicking outside
    $(document).click(function (event) {
        if (!$(event.target).closest('.dropdown, .nested-dropdown').length) {
            $('.dropdown-content, .nested-dropdown-content').removeClass('active');
            $('.dropdown-toggle, .nested-dropdown-toggle').removeClass('active');
        }
    });
});
