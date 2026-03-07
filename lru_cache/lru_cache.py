# LRU Cache Implementation
# OrderedDict provides O(1) time complexity for get and put operations
# In this program, the methods move_to_end and popitem are used to implement the LRU cache eviction policy


from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # mark as recently used
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # remove the oldest item


# ---- demo ----

if __name__ == "__main__":
    cache = LRUCache(capacity=3)

    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(3, 30)
    print(cache.cache)          # {1: 10, 2: 20, 3: 30}

    print(cache.get(2))         # 20  — key 2 moves to end
    print(cache.cache)          # {1: 10, 3: 30, 2: 20}

    cache.put(4, 40)            # evicts key 1 (oldest)
    print(cache.cache)          # {3: 30, 2: 20, 4: 40}

    print(cache.get(1))         # -1  — was evicted
    print(cache.get(3))         # 30  — key 3 moves to end
    print(cache.cache)          # {2: 20, 4: 40, 3: 30}
