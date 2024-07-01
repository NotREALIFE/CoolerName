from flask import Flask, request, make_response
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    data = request.json
    if data and 'RedirectingServerTo' in data:
        target_url = data['RedirectingServerTo']
        
        # Extract the original data without "RedirectingServerTo"
        forwarded_data = {k: v for k, v in data.items() if k != 'RedirectingServerTo'}
        
        # Extract headers and cookies
        headers = dict(request.headers)
        cookies = request.cookies
        
        # Remove Host header to avoid potential issues
        headers.pop('Host', None)
        
        try:
            if request.method == 'POST':
                response = requests.post(target_url, json=forwarded_data, headers=headers, cookies=cookies)
            else:
                response = requests.get(target_url, params=forwarded_data, headers=headers, cookies=cookies)
            
            # Create a Flask response with the response from the target server
            flask_response = make_response(response.content, response.status_code)
            
            # Copy headers from the target server response
            for key, value in response.headers.items():
                flask_response.headers[key] = value
            
            return flask_response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error forwarding request: {e}")
            return 'Error forwarding request', 500
    else:
        return 'No RedirectingServerTo specified', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
