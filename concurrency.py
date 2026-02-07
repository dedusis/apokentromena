from concurrent.futures import ThreadPoolExecutor


def run_concurrent(dht, titles):
    def task(title):
            return dht.lookup(title)
    with ThreadPoolExecutor(max_workers=8) as ex:
        return list(ex.map(task, titles))
