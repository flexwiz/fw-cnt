## original config
import os
from flask_caching.backends.rediscache import RedisCache

def env(key, default=None):
    return os.getenv(key, default)

# Redis Base URL
REDIS_BASE_URL=f"{env('REDIS_PROTO')}://{env('REDIS_HOST')}:{env('REDIS_PORT')}"

# Redis URL Params
REDIS_URL_PARAMS = ""

# Build Redis URLs
CACHE_REDIS_URL = f"{REDIS_BASE_URL}/{env('REDIS_DB', 1)}{REDIS_URL_PARAMS}"
CELERY_REDIS_URL = f"{REDIS_BASE_URL}/{env('REDIS_CELERY_DB', 0)}{REDIS_URL_PARAMS}"

MAPBOX_API_KEY = env('MAPBOX_API_KEY', '')
CACHE_CONFIG = {
      'CACHE_TYPE': 'RedisCache',
      'CACHE_DEFAULT_TIMEOUT': 300,
      'CACHE_KEY_PREFIX': 'superset_',
      'CACHE_REDIS_URL': CACHE_REDIS_URL,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = True

class CeleryConfig:
  imports  = ("superset.sql_lab", )
  broker_url = CELERY_REDIS_URL
  result_backend = CELERY_REDIS_URL

CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
      host=env('REDIS_HOST'),
      port=env('REDIS_PORT'),
      key_prefix='superset_results',
)

# Setting timezone to UTC
os.environ['TZ'] = 'UTC'

# Default language FR
BABEL_DEFAULT_LOCALE = 'fr'


# secret
# Generate your own secret key for encryption. Use `openssl rand -base64 42` to generate a good key
SECRET_KEY = 'LxJgSoFfVfMbV/nPsLUhvypoK2FeSFCIt8EplizyhU2/YcBWICAHIO19'
