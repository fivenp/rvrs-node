import requests

def fetch_requests(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # Assuming api returns a json array of commands
    except requests.RequestException as e:
        print(f"Error fetching tasks: {e}")
        return []
