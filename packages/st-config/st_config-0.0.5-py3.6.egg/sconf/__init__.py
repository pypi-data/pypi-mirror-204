import os
import sys
import json
import logging

logger = logging.getLogger(__name__)

class Config(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename="config.json"):
        cls = type(self)
        if not hasattr(cls, "_init"):
            env_path = os.getenv("SCONF_PATH")
            if env_path is not None:
                logger.info(f"USE Config in {env_path}/{filename}")
                config_file = f"{env_path}/{filename}"
            else:
                context_root = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
                logger.info(f"USE Config in {context_root}/{filename}")
                config_file = f"{context_root}/{filename}"

            with open(config_file, encoding="UTF-8") as json_file:
                self.json_data = json.load(json_file)
                logger.info(f"Loading config.json for [{self.json_data.get('ENV')}] from {config_file}")
            cls._init = True

    def cfg(self, *keys):
        tmp = self.json_data
        try:
            for key in keys:
                tmp = tmp.get(key)
        except Exception as ex:
            logger.exception(f"exception : {ex}", ex)
            return None

        return tmp


if __name__ == "__main__":
    x = Config()
    y = Config()

    r = y.cfg("dart", "keys")
    print(r)

    v = x.cfg("message", "telegram", "channel")
    print(v)

    v = x.cfg("crawling_interval")
    print(v)