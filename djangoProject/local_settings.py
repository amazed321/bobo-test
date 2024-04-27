from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo11',
        'USER': 'root',
        'PASSWORD': '123321',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "22715",
        }
    }
}
############
# SESSIONS #
############
# Session存储在哪里？
# SESSION_ENGINE = "django.contrib.sessions.backends.db"

# 如果存储到文件中，文件的路径。
# SESSION_ENGINE = "django.contrib.sessions.backends.file"
# SESSION_FILE_PATH = None

# 存储到缓存
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"