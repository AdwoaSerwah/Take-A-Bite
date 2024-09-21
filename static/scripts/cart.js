/*$(document).ready(function() {
    // Handle the form submission for quantity changes (plus or minus)
    $(document).on('submit', '.quantity-form', function (event) {
        event.preventDefault();  // Prevent the default form submission

        const form = $(this);
        const actionButton = form.find('button[type="submit"].plus:focus, button[type="submit"].minus:focus'); // Get the focused button
        const action = actionButton.hasClass('plus') ? 'increment' : 'decrement';  // Determine action based on class
        const cartItem = form.closest('.cart-item');  // Get the parent menu item element
        const quantityElement = cartItem.find('.quantity');
        let quantity = parseInt(quantityElement.text().trim());

        console.log("Cart Item:", cartItem);
        console.log(quantityElement.text());
        console.log("Quantity: ", quantity);

        // Update the quantity based on the action
        if (action === 'increment') {
            if (quantity < 10) {
                quantity += 1;
            } else {
                console.log("Maximum quantity reached.");
                return; // Do not proceed if the quantity is 10 or more
            }
        } else if (action === 'decrement') {
            if (quantity > 1) {
                quantity -= 1;
            } else {
                console.log("Minimum quantity reached.");
                return; // Do not proceed if the quantity is 1 or less
            }
        }

        console.log("New Quantity: ", quantity);
        console.log("Action: ", action);

        // Perform AJAX request to update the quantity on the server
        $.ajax({
            url: form.attr('action'),  // Get the form action URL
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                action: action,  // "increment" or "decrement"
                quantity: quantity  // Updated quantity
            }),
            success: function(response) {
                if (response.success) {
                    // Hide or show the cart counter based on the number of items
                    if (response.cart_item_count === 0) {
                        $('#cart-counter').hide();
                        location.reload();
                    } else {
                        $('#cart-counter').show();
                    }

                    // Update the quantity displayed on the page
                    quantityElement.text(quantity);
            
                    // Update the total for the individual cart item using the total_item_price from the response
                    const itemTotalElement = cartItem.find('.cart-item-total span:last-child');
                    console.log("Total item price", response.total_item_price, typeof response.total_item_price);
                    itemTotalElement.text('GH₵ ' + response.total_item_price);
            
                    // Update the cart subtotal displayed on the page
                    $('.subtotal').text(response.cart_subtotal);
            
                    // Update the cart total if needed (assuming no additional fees)
                    $('.total').text(response.cart_subtotal);

                    // Update the cart counter in the header using cart_item_count from the response
                    $('#cart-counter').text(response.cart_item_count);
            

                    // Optionally disable/enable buttons based on the new quantity
                    const minusButton = cartItem.find('.minus');
                    const plusButton = cartItem.find('.plus');
            
                    // Disable the minus button if quantity is 1
                    if (quantity > 1) {
                        console.log('Quantity > 1')
                        minusButton.removeClass('faded-icon');
                        
                    } else {
                        console.log('Quantity < 1')
                        minusButton.addClass('faded-icon');
                    }
            
                    // Disable the plus button if quantity is 10
                    if (quantity < 10) {
                        plusButton.removeClass('faded-icon');
                        console.log('Quantity < 10')
                    } else {
                        console.log('Quantity > 10')
                        plusButton.addClass('faded-icon');
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error("Error updating quantity:", error);
                console.log("There was an issue updating the quantity. Please try again.");
            }
        });
    });

    $(document).on('submit', '.remove-item-form', function(event) {
        event.preventDefault();  // Prevent the default form submission
    
        const form = $(this);
        const cartItem = form.closest('.cart-item');  // Get the parent cart item element
    
        // Perform AJAX request to remove the item from the cart
        $.ajax({
            url: form.attr('action'),  // Get the form action URL
            method: 'POST',
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    // Hide or show the cart counter based on the number of items
                    if (response.cart_item_count === 0) {
                        $('#cart-counter').hide();
                        // Reload the page if the cart is empty
                        location.reload();
                    } else {
                        $('#cart-counter').show();
                    }

                    // Update the cart subtotal displayed on the page
                    $('.subtotal').text(parseFloat(response.cart_subtotal).toFixed(2));

                    //$('.subtotal').text(response.cart_subtotal);
            
                    // Update the cart total if needed (assuming no additional fees)
                    const totalAmount = parseFloat(response.cart_subtotal).toFixed(2);
                    $('.total').text(totalAmount);
            
                    // Update the cart counter in the header using cart_item_count from the response
                    $('#cart-counter').text(response.cart_item_count);
            
                    // Remove the item from the DOM
                    cartItem.remove();
                }
            },
            error: function(xhr, status, error) {
                console.error("Error removing item:", error);
                console.log("There was an issue removing the item. Please try again.");
            }
        });
    });
    
});*/


$(document).ready(function() {
    let subtotal = parseFloat($('.subtotal').text());  // Initial subtotal value

    // Handle the form submission for quantity changes (plus or minus)
    $(document).on('submit', '.quantity-form', function (event) {
        event.preventDefault();  // Prevent the default form submission

        const form = $(this);
        const actionButton = form.find('button[type="submit"].plus:focus, button[type="submit"].minus:focus'); // Get the focused button
        const action = actionButton.hasClass('plus') ? 'increment' : 'decrement';  // Determine action based on class
        const cartItem = form.closest('.cart-item');  // Get the parent menu item element
        const quantityElement = cartItem.find('.quantity');
        let quantity = parseInt(quantityElement.text().trim());

        // Update the quantity based on the action
        if (action === 'increment') {
            if (quantity < 10) {
                quantity += 1;
            } else {
                console.log("Maximum quantity reached.");
                return; // Do not proceed if the quantity is 10 or more
            }
        } else if (action === 'decrement') {
            if (quantity > 1) {
                quantity -= 1;
            } else {
                console.log("Minimum quantity reached.");
                return; // Do not proceed if the quantity is 1 or less
            }
        }

        // Perform AJAX request to update the quantity on the server
        $.ajax({
            url: form.attr('action'),  // Get the form action URL
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                action: action,  // "increment" or "decrement"
                quantity: quantity  // Updated quantity
            }),
            success: function(response) {
                if (response.success) {
                    // Update the quantity displayed on the page
                    quantityElement.text(quantity);
            
                    // Update the total for the individual cart item using the total_item_price from the response
                    const itemTotalElement = cartItem.find('.cart-item-total span:last-child');
                    itemTotalElement.text('GH₵ ' + response.total_item_price);
            
                    // Update the cart subtotal and total
                    updateCartSummary(response.cart_subtotal, response.cart_item_count);

                    // Optionally disable/enable buttons based on the new quantity
                    const minusButton = cartItem.find('.minus');
                    const plusButton = cartItem.find('.plus');
                    minusButton.toggleClass('faded-icon', quantity <= 1);
                    plusButton.toggleClass('faded-icon', quantity >= 10);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error updating quantity:", error);
                console.log("There was an issue updating the quantity. Please try again.");
            }
        });
    });

    $(document).on('submit', '.remove-item-form', function(event) {
        event.preventDefault();  // Prevent the default form submission
    
        const form = $(this);
        const cartItem = form.closest('.cart-item');  // Get the parent cart item element
    
        // Perform AJAX request to remove the item from the cart
        $.ajax({
            url: form.attr('action'),  // Get the form action URL
            method: 'POST',
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    // Reload the page if the cart is empty
                    if (response.cart_item_count === 0) {
                        location.reload();
                    } else {
                        // Update the cart subtotal and total
                        updateCartSummary(response.cart_subtotal, response.cart_item_count);
            
                        // Remove the item from the DOM
                        cartItem.remove();
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error("Error removing item:", error);
                console.log("There was an issue removing the item. Please try again.");
            }
        });
    });

    // Handle delivery/pickup selection
    $('#delivery-option').on('change', function() {
        const pickupId = $('#delivery-option option[data-name="pickup"]').val();
        const selectedOption = $(this).val();
        let deliveryPrice = 0;  // Default to 0 for pickup

        console.log("Pickup id: ", pickupId);
        console.log("Selected option: ", selectedOption);

        if (selectedOption !== pickupId) {
            // Extract the delivery price from the option text
            deliveryPrice = parseFloat($('option:selected', this).text().match(/\(GH₵ ([\d.]+)\)/)[1]);

            // Show the delivery price section
            //$('.cart-delivery').show();
            // Update the delivery price display
            $('.cart-delivery').addClass('visible');
        } else {
            // Hide the delivery price section if pickup is selected
            //$('.cart-delivery').hide();
            $('.cart-delivery').removeClass('visible'); // Remove visible class to hide it
        }

        // Update the delivery price and total in the UI
        updateDeliveryAndTotal(deliveryPrice);
    });

    // Function to update cart subtotal and total
    function updateCartSummary(cartSubtotal, cartItemCount) {
        // Update the cart subtotal displayed on the page
        $('.subtotal').text(parseFloat(cartSubtotal).toFixed(2));

        // Update the cart total if needed (assuming no additional fees)
        const deliveryPrice = parseFloat($('.delivery').text()) || 0;
        const totalAmount = parseFloat(cartSubtotal) + deliveryPrice;
        $('.total').text(totalAmount.toFixed(2));

        // Update the cart counter in the header
        $('#cart-counter').text(cartItemCount);

        // Hide or show the cart counter based on the number of items
        $('#cart-counter').toggle(cartItemCount > 0);
    }

    // Function to update delivery price and total
    function updateDeliveryAndTotal(deliveryPrice) {
        // Update the delivery price in the UI
        $('.delivery').text(deliveryPrice.toFixed(2));

        // Update the total (subtotal + delivery price)
        const cartSubtotal = parseFloat($('.subtotal').text());
        const total = cartSubtotal + deliveryPrice;
        $('.total').text(total.toFixed(2));
    }

    /*$('#checkout-form').on('submit', function(event) {
        event.preventDefault();  // Prevent default form submission

        // Get the selected payment method
        const selectedPaymentMethod = $('input[name="payment_method"]:checked').val();

        // Create a JSON object with the form data
        const formData = {
            subtotal: parseFloat($('.subtotal').text()),  // Get the subtotal from the DOM
            total: parseFloat($('.total').text()),        // Get the total from the DOM
            delivery_fee: parseFloat($('.delivery').text()) || 0, // Get the delivery fee from the DOM, default to 0 if not present
            payment_method: selectedPaymentMethod         // Add the selected payment method
        };

        // Perform AJAX request to submit the form data
        $.ajax({
            url: $(this).attr('action'),  // Use form action URL
            method: 'POST',
            contentType: 'application/json',  // Set content type to JSON
            data: JSON.stringify(formData),   // Convert formData object to JSON string
            success: function(response) {
                if (response.success) {
                    // Redirect to checkout page on success
                    console.log("Back from ajax");
                    window.location.href = "/checkout";
                } else {
                    alert("Error processing checkout. Please try again.");
                }
            },
            error: function(xhr, status, error) {
                alert("An error occurred. Please try again. Error: ", error);
            }
        });
    });*/

    $('#checkout-form').on('submit', function(event) {
        event.preventDefault();  // Prevent default form submission
    
        // Get the selected payment method and delivery option
        const selectedPaymentMethod = $('input[name="payment_method"]:checked').val();
        const selectedLocationId = $('#delivery-option').val(); // Get selected location ID
    
        // Create a JSON object with the form data
        const formData = {
            subtotal: parseFloat($('.subtotal').text()),  // Get the subtotal from the DOM
            total: parseFloat($('.total').text()),        // Get the total from the DOM
            delivery_fee: parseFloat($('.delivery').text()) || 0, // Get the delivery fee from the DOM, default to 0 if not present
            payment_method: selectedPaymentMethod,        // Add the selected payment method
            location_id: selectedLocationId                // Add the selected location ID
        };
    
        // Perform AJAX request to submit the form data
        $.ajax({
            url: $(this).attr('action'),  // Use form action URL
            method: 'POST',
            contentType: 'application/json',  // Set content type to JSON
            data: JSON.stringify(formData),   // Convert formData object to JSON string
            success: function(response) {
                if (response.success) {
                    // Redirect to checkout page on success
                    console.log("Back from ajax");
                    window.location.href = "/checkout";
                } else {
                    alert("Error processing checkout. Please try again.");
                }
            },
            error: function(xhr, status, error) {
                alert("An error occurred. Please try again. Error: " + error);
            }
        });
    });
    
});

