import hashlib
from typing import Optional, Any, Dict, List, Tuple
from pathlib import Path
import random
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


# 1) Hashing to m-bit space
def hash_m(x: str, m: int) -> int:
    digest = hashlib.sha1(x.encode("utf-8")).hexdigest()  # string -> bytes -> sha1 hex
    return int(digest, 16) % (2 ** m)


# 2) Ring interval helper (wrap-around)
def in_interval(x: int, a: int, b: int, inclusive_right: bool = True) -> bool:
    if a == b:
        return True

    if a < b:
        return (a < x <= b) if inclusive_right else (a < x < b)
    else:
        # wrap-around
        return (x > a or x <= b) if inclusive_right else (x > a or x < b)


# 3) Finger table entry structure
class FingerEntry:
    def __init__(self, start: int, node=None):
        self.start = start
        self.node = node


# 4) Chord Node
class ChordNode:
    def __init__(self, name: str, m: int):
        self.name = name
        self.m = m
        self.ring_size = 2 ** m

        self.node_id = hash_m(name, m)

        self.successor: "ChordNode" = self
        self.predecessor: Optional["ChordNode"] = None

        self.store: Dict[int, Any] = {}

        self.finger: List[FingerEntry] = []
        self._init_finger_table()
        self._next_finger = 0

    def _init_finger_table(self) -> None:
        self.finger.clear()
        for i in range(1, self.m + 1):
            start = (self.node_id + (2 ** (i - 1))) % self.ring_size
            self.finger.append(FingerEntry(start=start, node=self))

    def __repr__(self) -> str:
        return f"ChordNode(name={self.name!r}, id={self.node_id})"

    # Routing core 
    def closest_preceding_finger(self, target_id: int) -> "ChordNode":
        for i in range(self.m - 1, -1, -1):
            fn = self.finger[i].node
            if fn is None:
                continue
            if in_interval(fn.node_id, self.node_id, target_id, inclusive_right=False):
                return fn
        return self

    def find_successor(self, target_id: int, hops: Optional[Dict[str, int]] = None) -> "ChordNode":
        if hops is not None:
            hops["hops"] += 1

        if self.successor == self:
            return self

        if in_interval(target_id, self.node_id, self.successor.node_id, inclusive_right=True):
            return self.successor

        next_node = self.closest_preceding_finger(target_id)
        if next_node == self:
            next_node = self.successor

        return next_node.find_successor(target_id, hops=hops)

    # Join / maintenance
    def join(self, bootstrap: Optional["ChordNode"]) -> None:
        if bootstrap is None:
            self.predecessor = None
            self.successor = self
            for fe in self.finger:
                fe.node = self
            return

        self.predecessor = None
        self.successor = bootstrap.find_successor(self.node_id)
        self.finger[0].node = self.successor

    def stabilize(self) -> None:
        x = self.successor.predecessor
        if x is not None and in_interval(x.node_id, self.node_id, self.successor.node_id, inclusive_right=False):
            self.successor = x
            self.finger[0].node = x
        self.successor.notify(self)

    def notify(self, nprime: "ChordNode") -> None:
        if self.predecessor is None:
            self.predecessor = nprime
            return
        if in_interval(nprime.node_id, self.predecessor.node_id, self.node_id, inclusive_right=False):
            self.predecessor = nprime

    def fix_fingers(self) -> None:
        i = self._next_finger
        start = self.finger[i].start
        self.finger[i].node = self.find_successor(start)
        self._next_finger = (self._next_finger + 1) % self.m

    #  DHT operations 
    def put(self, key: str, value: Any, hops: Optional[Dict[str, int]] = None) -> int:
        key_id = hash_m(key, self.m)
        owner = self.find_successor(key_id, hops)
        owner.store[key_id] = value
        return key_id

    def get(self, key: str, hops: Optional[Dict[str, int]] = None) -> Optional[Any]:
        key_id = hash_m(key, self.m)
        owner = self.find_successor(key_id, hops)
        return owner.store.get(key_id)

    def delete_key(self, key: str, hops: Optional[Dict[str, int]] = None) -> bool:
        key_id = hash_m(key, self.m)
        owner = self.find_successor(key_id, hops)
        if key_id in owner.store:
            del owner.store[key_id]
            return True
        return False

    def leave(self) -> None:
        if self.successor == self:
            self.store.clear()
            return

        # 1) Transfer keys to successor
        self.successor.store.update(self.store)
        self.store.clear()

        # 2) Repair ring pointers
        if self.predecessor is not None:
            self.predecessor.successor = self.successor
        self.successor.predecessor = self.predecessor

        # 3) Isolate
        self.successor = self
        self.predecessor = None


# Dataset / Network utils

ROOT = Path(r"C:/Users/user/Desktop/CEID THINGS/Αποκεντρωμένα")
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_FILE = DATA_DIR / "data_movies_clean.csv"

MOVIE_COLS_14 = [
    "id", "title", "adult", "original_language", "origin_country", "release_date",
    "genre_names", "production_company_names", "budget", "revenue", "runtime",
    "popularity", "vote_average", "vote_count"
]


def stabilize_network(nodes: List[ChordNode], rounds: int = 40) -> None:
    for _ in range(rounds):
        for n in nodes:
            n.stabilize()
        for n in nodes:
            n.fix_fingers()


def create_network(num_nodes: int, m: int) -> List[ChordNode]:
    nodes: List[ChordNode] = []
    n0 = ChordNode("node-0", m)
    n0.join(None)
    nodes.append(n0)

    for i in range(1, num_nodes):
        ni = ChordNode(f"node-{i}", m)
        bootstrap = random.choice(nodes)
        ni.join(bootstrap)
        nodes.append(ni)

    stabilize_network(nodes, rounds=50)
    return nodes


def row_to_value(row: pd.Series) -> Dict[str, Any]:
    return {c: (row[c] if c in row else None) for c in MOVIE_COLS_14}


def stats(hops: List[int]) -> Dict[str, float]:
    if not hops:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}
    return {"avg": sum(hops) / len(hops), "min": float(min(hops)), "max": float(max(hops))}


# Operation evaluations 

def eval_insert(nodes: List[ChordNode], df: pd.DataFrame, n_ops: int) -> Tuple[Dict[str, float], float, List[str]]:
    n_ops = min(n_ops, len(df))
    sample_df = df.sample(n=n_ops, random_state=1).reset_index(drop=True)

    hops_list: List[int] = []
    titles: List[str] = []
    t0 = time.time()

    for _, row in sample_df.iterrows():
        key = str(row["title"])
        value = row_to_value(row)

        entry = random.choice(nodes)
        hops = {"hops": 0}
        entry.put(key, value, hops=hops)

        hops_list.append(hops["hops"])
        titles.append(key)

    t1 = time.time()
    return stats(hops_list), (t1 - t0), titles


def eval_lookup(nodes: List[ChordNode], titles: List[str], n_ops: int) -> Tuple[Dict[str, float], float]:
    if not titles:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}, 0.0

    hops_list: List[int] = []
    t0 = time.time()

    for _ in range(n_ops):
        key = random.choice(titles)
        entry = random.choice(nodes)

        hops = {"hops": 0}
        _ = entry.get(key, hops=hops)
        hops_list.append(hops["hops"])

    t1 = time.time()
    return stats(hops_list), (t1 - t0)


def eval_delete(nodes: List[ChordNode], titles: List[str], n_ops: int) -> Tuple[Dict[str, float], float]:
    if not titles:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}, 0.0

    n_ops = min(n_ops, len(titles))
    keys_to_delete = random.sample(titles, k=n_ops)

    hops_list: List[int] = []
    t0 = time.time()

    for key in keys_to_delete:
        entry = random.choice(nodes)
        hops = {"hops": 0}
        _ = entry.delete_key(key, hops=hops)
        hops_list.append(hops["hops"])

    t1 = time.time()
    return stats(hops_list), (t1 - t0)


def eval_join(nodes: List[ChordNode], m: int, n_ops: int) -> Tuple[Dict[str, float], float]:
    hops_list: List[int] = []
    t0 = time.time()

    for i in range(n_ops):
        new_node = ChordNode(f"node-new-{int(time.time() * 1000) % 10_000}_{i}", m)
        bootstrap = random.choice(nodes)

        hops = {"hops": 0}
        _ = bootstrap.find_successor(new_node.node_id, hops=hops)
        new_node.join(bootstrap)
        nodes.append(new_node)

        stabilize_network(nodes, rounds=10)
        hops_list.append(hops["hops"])

    t1 = time.time()
    return stats(hops_list), (t1 - t0)


def eval_leave(nodes: List[ChordNode], n_ops: int) -> Tuple[Dict[str, float], float]:
    if len(nodes) <= 1:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}, 0.0

    n_ops = min(n_ops, len(nodes) - 1)
    victims = random.sample(nodes, k=n_ops)

    hops_list: List[int] = []
    t0 = time.time()

    for v in victims:
        if v.successor == v:
            continue
        v.leave()
        nodes[:] = [n for n in nodes if n is not v]
        stabilize_network(nodes, rounds=10)
        hops_list.append(0)  # graceful leave: no routing

    t1 = time.time()
    return stats(hops_list), (t1 - t0)


# Concurrent K popularity lookups 

def lookup_popularity(nodes: List[ChordNode], title: str) -> Tuple[str, Optional[float], int]:
    entry = random.choice(nodes)
    hops = {"hops": 0}
    value = entry.get(title, hops=hops)

    if value is None:
        return (title, None, hops["hops"])

    pop = value.get("popularity", None)
    try:
        pop = float(pop) if pop is not None else None
    except Exception:
        pop = None

    return (title, pop, hops["hops"])


def concurrent_popularity_lookup(
    nodes: List[ChordNode],
    titles: List[str],
    K: int = 10,
    max_workers: Optional[int] = None
) -> Tuple[List[Tuple[str, Optional[float]]], Dict[str, float]]:

    if not titles:
        return [], {"avg": 0.0, "min": 0.0, "max": 0.0}

    K = max(1, min(K, len(titles)))
    chosen = titles[:K]
    max_workers = max_workers or K

    hop_list: List[int] = []
    out: List[Tuple[str, Optional[float]]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(lookup_popularity, nodes, t) for t in chosen]
        for f in as_completed(futures):
            title, pop, hops = f.result()
            out.append((title, pop))
            hop_list.append(hops)

    out.sort(key=lambda x: chosen.index(x[0]) if x[0] in chosen else 10**9)
    return out, stats(hop_list)



if CSV_FILE.exists():
    print(f"Reading CSV: {CSV_FILE}...")
    df_raw = pd.read_csv(CSV_FILE, encoding="latin1")

    cols_present = [c for c in MOVIE_COLS_14 if c in df_raw.columns]
    if "title" not in cols_present:
        raise SystemExit("CSV must contain 'title' column.")

    df = df_raw[cols_present].dropna(subset=["title"]).copy().reset_index(drop=True)
    print(f"Loaded {len(df)} rows. Columns used: {cols_present}")

    # --- experiment parameters ---
    m = 16
    num_nodes = 50

    insert_ops = 5000
    lookup_ops = 5000
    delete_ops = 2000
    join_ops = 20
    leave_ops = 20

    print("\nBuilding Chord network...")
    nodes = create_network(num_nodes=num_nodes, m=m)

    print("\n=== EVALUATION (Chord) ===")

    ins_stats, ins_time, inserted_titles = eval_insert(nodes, df, n_ops=insert_ops)
    print(f"INSERT: {ins_stats} | time={ins_time:.3f}s")

    # CONCURRENT LOOKUP (K titles)
    print("\n--- Concurrent Popularity Lookup (K titles) ---")
    try:
        K = int(input("Δώσε K (π.χ. 10): ").strip())
    except Exception:
        K = 10

    if inserted_titles:
        chosen_titles = random.sample(inserted_titles, k=min(K, len(inserted_titles)))
        results, hop_stats = concurrent_popularity_lookup(nodes, chosen_titles, K=len(chosen_titles))

        print("\nΑποτελέσματα (title -> popularity):")
        for t, p in results:
            print(f"- {t} -> {p}")

        print(f"\nRouting hops για τα {len(chosen_titles)} concurrent lookups:")
        print(hop_stats)
    else:
        print("Δεν υπάρχουν inserted titles για concurrent lookup.")

    # continue with the remaining operations normally
    look_stats, look_time = eval_lookup(nodes, inserted_titles, n_ops=lookup_ops)
    print(f"LOOKUP: {look_stats} | time={look_time:.3f}s")

    del_stats, del_time = eval_delete(nodes, inserted_titles, n_ops=delete_ops)
    print(f"DELETE: {del_stats} | time={del_time:.3f}s")

    join_stats, join_time = eval_join(nodes, m=m, n_ops=join_ops)
    print(f"JOIN  : {join_stats} | time={join_time:.3f}s")

    leave_stats, leave_time = eval_leave(nodes, n_ops=leave_ops)
    print(f"LEAVE : {leave_stats} | time={leave_time:.3f}s  (routing hops=0 in graceful leave)")

else:
    print(f"CSV not found: {CSV_FILE}")

