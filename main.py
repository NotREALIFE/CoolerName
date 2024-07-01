from flask import Flask, request, redirect, make_response
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if 'RedirectingServerTo' in request.values:
        target_url = request.values['RedirectingServerTo']
        
        # Extract the original data without "RedirectingServerTo"
        forwarded_data = {k: v for k, v in request.values.items() if k != 'RedirectingServerTo'}
        
        # Extract headers and cookies
        headers = dict(request.headers)
        cookies = request.cookies
        
        # Remove Host header to avoid potential issues
        headers.pop('Host', None)
        
        if request.method == 'POST':
            response = requests.post(target_url, data=forwarded_data, headers=headers, cookies=cookies)
        else:
            response = requests.get(target_url, params=forwarded_data, headers=headers, cookies=cookies)
        
        # Create a Flask response with the response from the target server
        flask_response = make_response(response.content, response.status_code)
        
        # Copy headers from the target server response
        for key, value in response.headers.items():
            flask_response.headers[key] = value
        
        return flask_response
    
    return 'No RedirectingServerTo specified', 400

if __name__ == '__main__':
    app.run(debug=True)
