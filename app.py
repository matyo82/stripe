from flask import Flask, redirect, request
import stripe
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['payment_database']
app = Flask(__name__, static_url_path="", static_folder="public")

stripe.api_key = "sk_test_51OAZypGHbzUCy9HwgQ9jxP2fSY5kj7IJeXq8vAIeZTI3n9XDbLMa4mWI8IRkqZwYJmSypyfLQWay3Q95q15L4Swb009OQTVl6v"
YOUR_DOMAIN = "127.0.0.1:5000"


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OAx6lGHbzUCy9HwvXObReUH',
                    'quantity': 1,
                }
            ],
            mode="payment",
            success_url="http://127.0.0.1:5000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://127.0.0.1:5000/cancel.html"
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    session_id = request.args.get('session_id')
    # if not set session_id
    if not session_id:
        return 'Error: No session ID provided'

    # ذخیره session_id در دیتابیس
    db.payment_info.insert_one({'session_id': session_id})

    return f'Success! Session ID: {session_id}'

if __name__ == "__main__":
    app.run(port=5000, debug=True)
