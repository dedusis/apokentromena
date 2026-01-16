from concurrent.futures import ThreadPoolExecutor

def run_concurrent(dht, titles):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(dht.lookup, t) for t in titles]
        return [f.result() for f in futures]
