import stripe

# Set your secret key
stripe.api_key = "sk_test_51N04GUDoIaCywcQMysqyLjL4aQVm6PU2WanfkrFdm0iG0bmlfvBmEu13cBVSQBtOwQyrmkJ9trS1mWU2jGUX8xJC00BQdhZq7j"


# Create a payment
def create_payment(amount, token):
    try:
        # Charge the customer's card
        charge = stripe.Charge.create(
            amount=amount,
            currency="euro",
            source=token,
            description="Resort Booking Payment"
        )
        return charge
    except stripe.error.CardError as e:
        # Card was declined
        return e
