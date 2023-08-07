import env

BOT_TOKEN = env.get("BOT_TOKEN")
APP_PORT = env.get_int("APP_PORT", 80)
APP_URL = env.get("APP_URL")


class MONGO:
    _ = "MONGO_"
    DB = env.get(_ + "DB")
    HOST = env.get(_ + "HOST")
    USER = env.get(_ + "USER", "root")
    PASSWORD = env.get(_ + "PASSWORD")
