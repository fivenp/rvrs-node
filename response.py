import requests

def post_response(url, result):
    try:
        response = requests.post(url, json=result)
        response.raise_for_status()
        return response.json()  # Asuming api returns a json array of commands
    except requests.RequestException as e:
        print(f"Error posting result for command '{result['command']}': {e}")
        return None
