from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check_card():
    number = request.args.get('number')
    expiration_month = request.args.get('expiration_month')
    expiration_year = request.args.get('expiration_year')
    cvv = request.args.get('cvv')
    
    # Set your headers and request data
    headers = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MjcyMzMwNDcsImp0aSI6IjNmMjcyZjExLTYyMzQtNGFhNy04MTM4LWIwODZkZjA1MzM0ZiIsInN1YiI6ImR3azVzcGRndzdxc2Nka3AiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6ImR3azVzcGRndzdxc2Nka3AiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJtYW5hZ2VfdmF1bHQiXSwic2NvcGUiOlsiQnJhaW50cmVlOlZhdWx0Il0sIm9wdGlvbnMiOnsibWVyY2hhbnRfYWNjb3VudF9pZCI6ImF1dG9vbmV0cmFkaW5nQVVEM0RTMiJ9fQ.FCXYFFI-28SGvQWfd8npLXt_XQmBbzY0fM8u39_4dKcDMFanlhsk8aDpHVHPFrO2IxFn93yjHklZADre1uUpmA',
        'braintree-version': '2018-05-10',
        'content-type': 'application/json',
    }

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'dropin2',
            'sessionId': '8cb8ee81-5dc6-4aba-bd10-e7f83dcd5362',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': number,
                    'expirationMonth': expiration_month,
                    'expirationYear': expiration_year,
                    'cvv': cvv,
                    'cardholderName': 'Test User',
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
    
    # Process response to filter required statuses
    response_data = response.json()
    statuses = ['lookup_error', 'authenticate_rejected', 'challenge_required', 'authenticate_successful', 'authenticate_attempt_successful']
    filtered_response = {status: response_data.get(status) for status in statuses if status in response_data}

    return jsonify(filtered_response), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)