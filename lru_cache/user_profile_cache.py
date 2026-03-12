# User Profile Cache with TTL
# Simulates a slow "get user profile" API endpoint and adds an in-memory
# caching layer.  Each cached entry expires after a configurable TTL
# (time-to-live) so stale data is automatically refreshed.

import time


# ---------- simulated slow backend ----------

USER_DB = {
    101: {"name": "Alice", "email": "alice@example.com", "role": "admin"},
    102: {"name": "Bob", "email": "bob@example.com", "role": "editor"},
    103: {"name": "Charlie", "email": "charlie@example.com", "role": "viewer"},
}


def slow_get_user(user_id):
    """Pretend this is a slow database / network call."""
    time.sleep(1)
    return USER_DB.get(user_id)


# ---------- cache ----------

class ProfileCache:
    def __init__(self, ttl: int = 5):
        self.ttl = ttl                  # seconds before an entry expires
        self.cache: dict = {}           # {user_id: (profile, timestamp)}

    def get(self, user_id):
        if user_id in self.cache:
            profile, ts = self.cache[user_id]
            if time.time() - ts < self.ttl:
                return profile          # cache hit
            del self.cache[user_id]     # expired → remove
        return None                     # cache miss

    def put(self, user_id, profile):
        self.cache[user_id] = (profile, time.time())

    def get_user_profile(self, user_id):
        cached = self.get(user_id)
        if cached is not None:
            print(f"  [CACHE HIT]  user {user_id}")
            return cached

        print(f"  [CACHE MISS] user {user_id} — fetching …")
        profile = slow_get_user(user_id)
        if profile is not None:
            self.put(user_id, profile)
        return profile


# ---------- demo ----------

if __name__ == "__main__":
    cache = ProfileCache(ttl=3)

    print("1st request (miss — slow):")
    t0 = time.time()
    print(f"  {cache.get_user_profile(101)}  ({time.time()-t0:.2f}s)\n")

    print("2nd request (hit — instant):")
    t0 = time.time()
    print(f"  {cache.get_user_profile(101)}  ({time.time()-t0:.2f}s)\n")

    print("Waiting 4s for TTL to expire …\n")
    time.sleep(4)

    print("3rd request (expired — slow again):")
    t0 = time.time()
    print(f"  {cache.get_user_profile(101)}  ({time.time()-t0:.2f}s)\n")

    print("Different user (miss):")
    t0 = time.time()
    print(f"  {cache.get_user_profile(102)}  ({time.time()-t0:.2f}s)")
