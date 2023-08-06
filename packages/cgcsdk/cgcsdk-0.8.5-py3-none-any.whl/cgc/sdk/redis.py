from redis import Redis, ConnectionError


class RedisConnector:
    def __init__(
        self, host: str, password: str = None, decode_responses: bool = False
    ) -> None:
        self._host = host
        assert type(host) is str
        "host must be a str containing redis app name"
        self._password = password
        self._decode_responses = decode_responses
        self.connect()

    def connect(self):
        while True:
            try:
                self._redis_client = Redis(
                    host=self._host,
                    port=6379,
                    password=self._password,
                    decode_responses=self._decode_responses,
                )
                print(f"Connected to Redis: {self._host}")
                break
            except (ConnectionError,) as e:
                print(f"Redis connection error: {e}")
                print(f"retrying to connect...")

    def get_redis_client(self):
        return self._redis_client


def get_redis_access(
    app_name: str, password: str, decode_responses: bool = False, restart: bool = False
):
    global _redis_access

    def init_access():
        global _redis_access
        _redis_access = RedisConnector(
            host=app_name, password=password, decode_responses=decode_responses
        )

    try:
        if not isinstance(_redis_access, RedisConnector) or restart:
            init_access()
    except NameError:
        init_access()
        pass
    return _redis_access
