if (response.success) {
    // Update the quantity displayed on the page
    quantityElement.text(quantity);

    // Optionally disable/enable buttons based on the new quantity
    const minusButton = cartItem.find('.quantity-btn.minus');
    const plusButton = cartItem.find('.quantity-btn.plus');

    // Disable the minus button if quantity is 1
    if (quantity === 1) {
        minusButton.addClass('faded-icon');
    } else {
        minusButton.removeClass('faded-icon');
    }

    // Disable the plus button if quantity is 10
    if (quantity === 10) {
        plusButton.addClass('faded-icon');
    } else {
        plusButton.removeClass('faded-icon');
    }
}