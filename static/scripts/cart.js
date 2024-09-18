document.getElementById('delivery-method').addEventListener('change', function() {
    const locationContainer = document.getElementById('location-container');
    const totalElement = document.getElementById('total');
    const subtotal = parseFloat('{{ cart_subtotal }}');

    if (this.value === 'delivery') {
        locationContainer.style.display = 'block';  // Show location dropdown for delivery
    } else {
        locationContainer.style.display = 'none';   // Hide location dropdown for pickup
        totalElement.innerText = subtotal.toFixed(2);  // Reset to subtotal
    }
});

document.getElementById('location').addEventListener('change', function() {
    const deliveryPrice = parseFloat(this.selectedOptions[0].getAttribute('data-price'));
    const subtotal = parseFloat('{{ cart_subtotal }}');
    const total = subtotal + deliveryPrice;

    document.getElementById('total').innerText = total.toFixed(2);  // Update total with delivery price
});

const deliveryDropdown = document.querySelector('.delivery-select-wrapper');
const deliverySelectBtn = document.querySelector('.delivery-select-btn');
const deliveryDropdownContent = document.querySelector('.delivery-dropdown-content');

// Toggle dropdown open/close
deliverySelectBtn.addEventListener('click', function () {
    deliveryDropdown.classList.toggle('active');
    deliveryDropdownContent.style.display = deliveryDropdownContent.style.display === 'block' ? 'none' : 'block';
});

// Select dropdown option and display in button
deliveryDropdownContent.addEventListener('click', function (e) {
    if (e.target && e.target.nodeName === "DIV") {
        deliverySelectBtn.textContent = e.target.textContent; // Update button text
        deliveryDropdownContent.style.display = 'none'; // Close the dropdown
        deliveryDropdown.classList.remove('active');
        console.log('Selected value:', e.target.getAttribute('data-value')); // Log the selected value (you can use this for form submissions)
    }
});

// Close dropdown if clicked outside
window.addEventListener('click', function (e) {
    if (!deliveryDropdown.contains(e.target)) {
        deliveryDropdownContent.style.display = 'none';
        deliveryDropdown.classList.remove('active');
    }
});
