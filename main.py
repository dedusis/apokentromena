def main():
    dht = load_dht("chord")   # ή pastry
    dht.build(nodes=50)

    for movie in dataset:
        dht.insert(movie.key, movie.value)

    result = dht.lookup("Inception")
