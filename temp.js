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



Here's a longer description for the inspiration behind the project:

Inspiration Behind Take-A-Bite:

Take-A-Bite was born from a blend of passion and necessity. Living in Accra, I’ve always been fascinated by how food can bring people together, but I often found myself frustrated by the lack of streamlined food pick-up and delivery services that catered to the diverse and vibrant food culture here. Whether it was long wait times, the challenge of keeping track of orders, or limited delivery options, I saw an opportunity to make a change.

The idea for Take-A-Bite came to me while balancing my daily commitments and the desire for quick, reliable food services that didn't compromise on quality. I wanted to create something that felt tailored for the people of Accra—a platform that not only celebrates local cuisine but also provides an efficient, seamless experience for users, whether they’re ordering a simple meal or indulging in their favorite dish.

From the early conceptual stages, I envisioned Take-A-Bite as more than just a food delivery service. It’s designed to support local restaurants and provide a space for customers to explore new flavors while ensuring they can pick up their orders or get them delivered in the fastest, most convenient way. This project also serves as my capstone for Holberton School, where I’ve honed my skills in software development, balancing real-world user needs with technical execution. You can find the source code and more about the journey behind building this platform here.

