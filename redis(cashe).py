import redis
import json

r = redis.Redis()

def cache_search(key, search_function, *args):
    cached_result = r.get(key)
    if cached_result:
        print(json.loads(cached_result.decode('utf-8')))
    else:
        result = search_function(*args)
        r.set(key, json.dumps(result), ex=3600)
        print(result)


