import subprocess

from request import *
from response import *

def get_and_execute_request(id):
    # Fetch list of tasks (commands)
    print("🚢 New request for me....")





    requests = fetch_requests(REQUESTS_URL)
    if not requests:
        print("No requests fetched. Exiting.")
        return

    # Iterate over each command and execute it
    for request in requests:
        command = request.get("command")
        if command:
            print(f"Executing command: {command}")

            # Execute the command and get the result
            result = execute_command(command)

            # Post the result to the API
            print(f"Posting result for command: {command}")
            post_response("http://localhost:8787/response", result)

            print(f'Result for "{command}": {result["status"]}\n')
        else:
            print("Invalid request received, skipping.")

def execute_request(apiUrl,nodeId,requestId,type,options,dest):
    print("🚢 Executing request....")
    command = "ping -t 6"
    if ('MTR' in type):
        command = "mtr --raw -n -4 -c 10"
        command = "mtr -w -z -4 -c 6"
        #command = "traceroute -4 -w2 -m30"
        #command = "traceroute -w2 -m30"
    if ('IPERF' in type):
        command = "iperf -c"
    # if ('BGP' in type):
    #     command = "bgp"
    if ('DIG' in type):
        command = "dig"

    fullCmd = command + " "+options+" "+dest
    print(fullCmd)
    result = execute_command(fullCmd)
    # print(result)

    if "status" in result:
        if ("error" in result["status"]):
            print(f"🧨 Command run failed....")
            print(result["error"])

        print(f"🚀 Posting result for command: {fullCmd}")
        data = {
            "response": result,
            "requestId": requestId,
            "nodeId": nodeId
        }
        #print(data)
        post_response(f"{apiUrl}/response", data)
        print(f"✅ Result posted")


def execute_command(command):
    # Execute shell command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        error = result.stderr.decode("utf-8")
        return {
            "command": command,
            "output": output,
            "error": error,
            "status": "success"
        }
    except subprocess.CalledProcessError as e:
        return {
            "command": command,
            "output": e.stdout.decode("utf-8") if e.stdout else "",
            "error": e.stderr.decode("utf-8") if e.stderr else str(e),
            "status": "error"
        }
