let paymentInProgress = false;

$(document).ready(function() {
    $('#payment-form').on('submit', function(e) {
        e.preventDefault(); // Prevent the form from submitting normally
        paymentInProgress = true; // Set payment in progress to true

        // Retrieve data from the button's data-* attributes
        let totalAmount = $('#paystackButton').data('total') * 100; // Paystack requires amount in kobo/pesewas
        let email = $('#paystackButton').data('email'); // Use the user's email to send the receipt
        let orderID = $('#paystackButton').data('order-id'); // Retrieve order ID
        let username = $('#paystackButton').data('username'); // Retrieve username
        let updatePaymentUrl = $(this).attr('action');

        var handler = PaystackPop.setup({
            key: 'pk_test_3172601967078640096a6f10075e6537df112f15', // Replace with your Paystack public key
            email: email,
            amount: totalAmount,
            currency: "GHS",
            ref: orderID + '-' + Math.floor((Math.random() * 1000000000) + 1), // Unique reference for the transaction
            metadata: {
                custom_fields: [
                    {
                        display_name: "Username",
                        variable_name: "username",
                        value: username // Now we use the username from data-attribute
                    },
                    {
                        display_name: "Order ID",
                        variable_name: "order_id",
                        value: orderID
                    }
                ]
            },
            callback: function(response) {
                // When payment is successful, update the database
                $.ajax({
                    url: updatePaymentUrl,
                    type: 'POST',
                    contentType: 'application/json', // Specify content type as JSON
                    data: JSON.stringify({
                        order_id: orderID,
                        payment_status: 'COMPLETED',
                        transaction_ref: response.reference
                    }),
                    success: function(data) {
                        if (data.message) {
                            // window.location.href = "/order-status";
                            console.log("Order id: ", orderID);
                            window.location.href = `/order-confirmed?order_id=${orderID}`;
                        }
                        else {
                            alert(data.error);
                        }
                    },
                    error: function() {
                        console.log('Payment was successful but failed to update the server.');
                    }
                });
            },
            onClose: function() {
                // Handle the cancellation here
                if (paymentInProgress) {
                    $.ajax({
                        url: updatePaymentUrl,
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify({
                            order_id: orderID,
                            payment_status: 'CANCELLED' // Update the payment status to cancelled
                        }),
                        success: function(data) {
                            if (data.message)
                                alert("Payment was cancelled. Please try again");
                            else {
                                alert(data.error);
                            }
                        },
                        error: function() {
                            console.error('Failed to update payment status on cancellation.');
                        }
                    });
                }
            }
        });

        handler.openIframe(); // Open the Paystack payment interface
    });
});
