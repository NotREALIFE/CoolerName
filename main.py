from flask import Flask, request, make_response
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['POST'])
def handle_request():
    target_url = None
    data = request.json
    
    if data and 'RedirectingServerTo' in data:
        target_url = data['RedirectingServerTo']
        forwarded_data = {k: v for k, v in data.items() if k != 'RedirectingServerTo'}
        
        headers = {key: value for key, value in request.headers.items() if key != 'Host'}
        cookies = request.cookies
        
        try:
            if request.method == 'POST':
                response = requests.post(target_url, json=forwarded_data, headers=headers, cookies=cookies, timeout=10)
            else:
                response = requests.get(target_url, params=forwarded_data, headers=headers, cookies=cookies, timeout=10)
                
            result = {'Text': response.text}
            return result, response.status_code
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error forwarding request: {e}")
            return 'Error forwarding request', 500
        
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            return 'Internal Server Error', 500
        
    else:
        return 'No RedirectingServerTo specified', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
