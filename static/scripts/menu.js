$(document).ready(function () {    
    // Decrement quantity
    window.decrementQuantity = function (button) {
        const menuItem = $(button).closest('.menu-item'); // Select the parent menu item

        // Check if the button is in "Add to Cart" state
        if (menuItem.find('.add-cart').length) {
            const quantityElement = menuItem.find('.quantity'); // Select quantity within the parent menu item
            const incrementButton = menuItem.find('.plus');
            let quantity = parseInt(quantityElement.text());

            if (quantity > 1) { // Ensure quantity doesn't go below 1
                quantity--;
                quantityElement.text(quantity); // Update the displayed quantity
                updateButtonAmount(menuItem); // Update the amount on the button

                // Enable plus button if it's faded
                if (quantity < 10) {
                    incrementButton.removeClass('faded-icon');
                    /*incrementButton.css('pointer-events', 'auto'); // Re-enable minus button*/
                }
            }

            // If quantity is below 1, add the faded class to minus button
            if (quantity === 1) {
                $(button).addClass('faded-icon');
                /*$(button).css('pointer-events', 'none');*/ // Disable minus button
            }
        }
    };

    // Increment quantity
    window.incrementQuantity = function (button) {
        const menuItem = $(button).closest('.menu-item'); // Select the parent menu item

        // Check if the button is in "Add to Cart" state
        if (menuItem.find('.add-cart').length) {
            const quantityElement = menuItem.find('.quantity'); // Select quantity within the parent menu item
            const decrementButton = menuItem.find('.minus');
            let quantity = parseInt(quantityElement.text());

            if (quantity < 10) { // Ensure quantity doesn't go above 10
                quantity++;
                quantityElement.text(quantity); // Update the displayed quantity
                updateButtonAmount(menuItem); // Update the amount on the button

                // If quantity is above 1, ensure the minus button is active
                if (quantity > 1) {
                    decrementButton.removeClass('faded-icon');
                    /*decrementButton.css('pointer-events', 'auto'); // Re-enable minus button*/
                }
            }

            // If quantity reaches 10, add the faded class to plus button
            if (quantity === 10) {
                $(button).addClass('faded-icon');
                /*$(button).css('pointer-events', 'none');*/ // Disable plus button
            }
        }
    };

    $(document).on('submit', '#add-to-cart-form', function (event) {
        event.preventDefault(); // Prevent the default form submission
    
        // Get form data
        const form = $(this);
        const menuItem = form.closest('.menu-item');
        const submitButton = form.find('button');
    
        // Check if the button is in "View Cart" mode
        if (submitButton.hasClass('view-cart')) {
            // Redirect to the cart page without making an AJAX request
            window.location.href = "/cart"; // Replace with your actual cart page URL
            return;  // Exit the function to prevent further execution
        }
    
        // Continue with the AJAX request if the button is in "Add to Cart" mode
        const menuItemId = form.find('input[name="menu_item_id"]').val();
        const quantityElement = menuItem.find('.quantity');
        const quantity = parseInt(quantityElement.text());
        const plusButton = menuItem.find('.quantity-btn.plus');
        const minusButton = menuItem.find('.quantity-btn.minus');
    
        console.log("Quantity: ", quantity);
    
        // Perform AJAX request to add the item to the cart
        $.ajax({
            url: form.attr('action'),  // Get the form action URL
            method: "POST",
            contentType: "application/json",  // Send as JSON
            data: JSON.stringify({
                menu_item_id: menuItemId,
                quantity: parseInt(quantity)
            }),
            success: function(response) {
    
                sessionStorage.removeItem('redirectUrl');
    
                if (submitButton.hasClass('add-cart')) {
                    // Update the header cart counter and display it
                    const headerCart = $('#cart-counter');
                    const currentTotal = parseInt(headerCart.text()) || 0;
                    
                    headerCart.text(currentTotal + parseInt(quantity));
                    headerCart.show(); // Show the cart counter        
                    // Change button text to "View Cart"
                    submitButton.text('View Cart')
                        .addClass('view-cart') // Add a class to style the "View Cart" button
                        .removeClass('add-cart'); // Remove the "Add Cart" class if it was present
    
                    // Add faded-icon class to plus and minus buttons
                    plusButton.addClass('faded-icon');
                    minusButton.addClass('faded-icon');
                }
            },
            error: function(xhr, status, error) {
                // Handle any errors
                if (xhr.status === 401 || xhr.status === 403) {
                    window.location.href = '/login';
                } else {
                    // Handle other errors
                    console.error("Error adding to cart:", error);
                    alert("There was an issue adding the item to your cart. Please try again.");
                }
            }
        });
    });
    

    // Function to update the "Add | Amount" button with dynamic amount
    function updateButtonAmount(menuItem) {
        const quantity = parseInt($(menuItem).find('.quantity').text());
        const priceText = $(menuItem).find('.price').text(); // Get the price text
        const price = parseFloat(priceText.replace('GH₵', '').trim()); // Convert the price text to a number
        const newAmount = price * quantity;
        $(menuItem).find('.add-cart .cart-col span:last-child').text('GH₵ ' + newAmount.toFixed(2));
    }

    // Toggle category filter
    $('.categories li').click(function() {
        //showSpinner(); // Show the spinner
        $('.categories li').removeClass('active');
        $(this).addClass('active');
        //hideSpinner();
       
        // Remove existing animation classes from menu items
        $('.menu-item').removeClass('flip-in');

        //filterMenuItems();

        // Delay adding animation class to create effect
        setTimeout(function() {
            filterMenuItems(); // Apply filter logic
            $('.menu-item').addClass('flip-in'); // Add animation class
        }, 500); // Adjust the delay as needed
    });

    // Search logic
    $('#menu-search-input').on('keypress', function(event) {
        if (event.which === 13) { // Check if Enter key is pressed
            event.preventDefault(); // Prevent form submission
            //showSpinner(); // Show the spinner
            filterMenuItems();
            $(this).blur();
        }
    });

    // Trigger filtering when the input changes (e.g., typing, deleting text, etc.)
    $('#menu-search-input').on('input', function() {
        filterMenuItems();
    });

    function filterMenuItems() {
        const searchQuery = $('#menu-search-input').val().toLowerCase().trim();
        const selectedCategory = $('.categories li.active').data('filter');
        const searchWords = searchQuery.split(' ');
        let foundInCategory = false;
        let hasPartialMatches = false;
        let suggestionItems = new Set(); // Use Set to avoid duplicate suggestions

        // If searchQuery is empty, display all items in the selected category
        if (searchQuery === '') {
            $('.menu-item').each(function() {
                const itemCategory = $(this).data('category');
                if (selectedCategory === 'all' || itemCategory === selectedCategory) {
                    $(this).show(); // Show all items in the selected category
                } else {
                    $(this).hide(); // Hide items not in the selected category
                }
            });
            $('.no-results-message').hide(); // Hide no-results message
            $('.suggestion-message').hide(); // Hide suggestion message
            $('.suggestion-list').hide(); // Hide suggestion list
            return; // Exit the function since no further filtering is needed
        }
        
        // Hide all items initially
        $('.menu-item').hide();
    
        // First pass: Check for exact matches
        $('.menu-item').each(function() {
            const itemCategory = $(this).data('category');
            const itemName = $(this).find('h2').text().toLowerCase();
            const matchesCategory = (selectedCategory === 'all' || itemCategory === selectedCategory);
            const matchesSearch = itemName.indexOf(searchQuery) !== -1;
    
            if (matchesCategory && matchesSearch) {
                $(this).show();
                foundInCategory = true;
            } else if (matchesCategory && searchWords.some(word => itemName.indexOf(word) !== -1)) {
                // Collect suggestions if no exact match found and prevent duplicates
                if (!suggestionItems.has(itemName)) {
                    suggestionItems.add(itemName);
                    $('.suggestion-list').append($(this).clone().show());
                }
                hasPartialMatches = true;
            }
        });
    
        // Display message if the item is not found
        if (!foundInCategory) {
            const selectedCategoryText = $('.categories li.active').text();
            const message = `No <b>${searchQuery}</b> found in <b>${selectedCategoryText}</b> category.`;
            
            // Show or hide no-results-message based on similar results
            if (hasPartialMatches) {
                $('.no-results-message').html(message).removeClass('no-results-partial').show(); // Apply partial results style
                $('.suggestion-message').html('Here are some items that might be of interest:').show();
                $('.suggestion-list').show(); // Display suggestion items
            } else {
                $('.no-results-message').html(message).addClass('no-results-partial').show(); // Apply full no results style
                $('.suggestion-message').hide(); // Hide suggestion message
                $('.suggestion-list').hide(); // Hide suggestion list
            }
        } else {
            $('.no-results-message').hide(); // Hide the message if results are found
            $('.suggestion-message').hide(); // Hide suggestion message
            $('.suggestion-list').hide(); // Hide suggestion list
        }

        //hideSpinner(); // Hide the spinner after filtering is done
    }
});
