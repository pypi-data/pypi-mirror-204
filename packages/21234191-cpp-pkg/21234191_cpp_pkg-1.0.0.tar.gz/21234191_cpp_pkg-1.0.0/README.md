Install the library using pip:

pip install my_payment_gateway_library

Usage
To use the library, import the create_payment function from the booking_properties package, and pass in the required parameters:

import my_payment_gateway_library

# Set up the Payment Gateway Provider configuration
gateway_config = {
    "api_key": "your_api_key",
    "other_option": "value"
}

# Create a payment using the Payment Gateway Library
payment = my_payment_gateway_library.create_payment(amount=1000, card_number="4242424242424242", config=gateway_config)

# Handle the payment response
if payment.status == "success":
    # Update the booking status or take other appropriate actions
    print("Payment successful!")
else:
    # Display an error message or take other appropriate actions
    print("Payment failed: ", payment.error_message)
