import argparse
import concurrent.futures
from scripts.Parser import Parser
from scripts.Requests import Requests


parser = argparse.ArgumentParser()

args = parser.add_argument("-u", "--url", help='Specify url, example: -u https://example.com/?param=value', nargs="+", type=str)
args = parser.add_argument("-l", "--list", help="Specify file with urls, example: -l urls.txt", type=str)
args = parser.add_argument("-t", "--thread", help="Specify threads number, example: -t 2", default=1, type=int)
args = parser.add_argument("-o", "--output", help="Specify output file, example: -o outputs.txt", type=str)

args = parser.parse_args()

def main():
    # Flags
    url = args.url
    file = args.list
    thread = args.thread
    output = args.output

    if file:
        url = open(file).read().splitlines()

    # Parser
    parsed_urls_params = []
    for parser_url in url:
        parser = Parser(parser_url)
        payload_read = open("./db/payloads.txt").read().splitlines()
        for payload in payload_read:
            parsed_urls = parser.parser_params(payload)
            if parsed_urls:
                parsed_urls_params.append(parsed_urls)

    # Requests
    req = Requests()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(req.requests, url) for url in parsed_urls_params]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if "root:" in result[0]:
                print(f"Directory traversal found -> \033[92m{result[1]}\033[00m")

if __name__ == "__main__":
    main()