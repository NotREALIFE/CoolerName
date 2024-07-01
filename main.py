from flask import Flask, request, make_response
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    target_url = None
    print("HI1")
    data = request.json
    print("data:", data)
    if data and 'RedirectingServerTo' in data:
        target_url = data['RedirectingServerTo']

        print("HI2", target_url)

        forwarded_data = {k: v for k, v in data.items() if k != 'RedirectingServerTo'}
        
        # Extract headers and cookies
        headers = {
            'User-Agent': request.headers.get('User-Agent', ''),
            'Accept': request.headers.get('Accept', '')
        }
        cookies = request.cookies
        
        print("OK")

        try:
            if request.method == 'POST':
                print("POST")
                response = requests.post(target_url, json=forwarded_data, headers=headers, cookies=cookies, timeout=10)
            else:
                print("ELSE", target_url, forwarded_data, headers, cookies)
                response = requests.get(str(target_url), params=forwarded_data, headers=headers, cookies=cookies, timeout=10)
                
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
