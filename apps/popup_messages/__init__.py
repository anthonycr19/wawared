import redis

# TODO: move to settings
redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
