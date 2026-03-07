# DNS Lookup Cache Implementation
# Every time your browser visits a website like google.com, it needs to look up the IP address (e.g. 142.250.190.14) from a DNS server. This lookup is slow (network round-trip). A real system caches these results so repeated visits are instant.
# Build a DNSCache that:
# Has a fixed capacity (say 3 entries).
# Has a resolve(domain) method:
# If the domain is in the cache, return the IP instantly (cache hit).
# If not, simulate a "slow DNS lookup", store the result, and return it (cache miss).
# When the cache is full, evict the least recently used domain.

import time
from collections import OrderedDict

# Simulates a slow DNS server (pretend this takes network time)
DNS_SERVER = {
    "google.com": "142.250.190.14",
    "github.com": "140.82.121.3",
    "stackoverflow.com": "151.101.1.69",
    "python.org": "138.197.63.241",
    "reddit.com": "151.101.65.140",
}


def slow_dns_lookup(domain):
    """Simulates a slow network call to resolve a domain."""
    time.sleep(1)  # pretend it takes 1 second
    return DNS_SERVER.get(domain, "0.0.0.0")

class DNSCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, domain):
        if domain is not None and domain in self.cache:
            self.cache.move_to_end(domain)
            return self.cache[domain]
    
    def put(self, domain, ip="0.0.0.0"):
        if domain is not None:
            self.cache[domain] = ip
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def resolve(self, domain):
        if domain is not None:
            if domain in self.cache:
                self.get(domain)
                print("cache hit, current cache: ", self.cache)
            else:
                ip = slow_dns_lookup(domain)
                self.put(domain, ip)
                print("cache miss, current cache: ", self.cache)

dnscache = DNSCache(capacity=4)

print(dnscache.resolve("google.com"))
print(dnscache.resolve("github.com"))
print(dnscache.resolve("google.com"))
print(dnscache.resolve("stackoverflow.com"))
print(dnscache.resolve("python.org"))
print(dnscache.resolve("reddit.com"))
