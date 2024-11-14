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

## ntdt override

from flask_appbuilder.security.manager import (AUTH_DB, AUTH_OAUTH)
AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
  {
      "name": "keycloak",
      "icon": "fa-key",
      "token_key": "access_token",
      "remote_app": {
          "client_id": 'sso-superset',
          "client_secret": 'Ngk8kds7iDpJ4bYZYRMgIVwolxAkiWQz',
          "api_base_url": 'http://keycloak:10000/auth/realms/ntdt/protocol/',
          "server_metadata_url": 'http://keycloak:10000/auth/realms/ntdt/.well-known/openid-configuration',
          "access_token_url": 'http://keycloak:10000/auth/realms/AOS/protocol/openid-connect/token',
          "authorize_url": 'http://keycloak:10000/auth/realms/AOS/protocol/openid-connect/auth',
          "client_kwargs":{
              'scope': 'openid email profile'
          },
      }
  }
]
AUTH_ROLES_MAPPING = {
  "Superset_Admin": ["Admin"],
  "Superset_Alpha": ["Alpha"],
  "Superset_Gamma": ["Gamma"]
}
# Map Authlib roles to superset roles
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
# Will allow user self registration, allowing to create Flask users from Authorized User
AUTH_USER_REGISTRATION = True
# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "AnalyticsDashboard"

## Custom security manager to get keycloak attribute
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Integer, Sequence, Table
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model

class CustomUser(User):
    __tablename__ = 'ab_user'
    headquarter = Column(String(256))
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from superset.security.manager import SupersetSecurityManager

log = logging.getLogger(__name__)

class CustomSecurityManager(SupersetSecurityManager):
    user_model = CustomUser
    # userdbmodelview = CustomUserDBModelView

    def get_oauth_user_info(self, provider: str, resp: Dict[str, Any]) -> Dict[str, Any]:
        # for Keycloak
        if provider in ["keycloak", "keycloak_before_17"]:
            me = self.appbuilder.sm.oauth_remotes[provider].get(
                "openid-connect/userinfo"
            )
            me.raise_for_status()
            data = me.json()
            log.debug("User info from Keycloak: %s", data)

            return {
                "username": data.get("preferred_username", ""),
                "first_name": data.get("given_name", ""),
                "last_name": data.get("family_name", ""),
                "email": data.get("email", ""),
                "headquarter": data.get("headquarter", None),
            }
        else:
            return super().get_oauth_user_info(provider, resp)


    def _oauth_calculate_user_roles(self, userinfo) -> List[str]:
        user_role_objects = set()

        # apply AUTH_ROLES_MAPPING
        if len(self.auth_roles_mapping) > 0:
            user_role_keys = userinfo.get("role_keys", [])
            user_role_objects.update(self.get_roles_from_keys(user_role_keys))

        # apply AUTH_USER_REGISTRATION_ROLE
        if self.auth_user_registration:
            registration_role_name = self.auth_user_registration_role

            # if AUTH_USER_REGISTRATION_ROLE_JMESPATH is set,
            # use it for the registration role
            if self.auth_user_registration_role_jmespath:
                import jmespath

                registration_role_name = jmespath.search(
                    self.auth_user_registration_role_jmespath, userinfo
                )

            # lookup registration role in flask db
            fab_role = self.find_role(registration_role_name)
            if fab_role:
                user_role_objects.add(fab_role)
            else:
                log.warning(
                    "Can't find AUTH_USER_REGISTRATION role: %s", registration_role_name
                )

        return list(user_role_objects)

    def auth_user_oauth(self, userinfo):
        """
        Method for authenticating user with OAuth.

        :userinfo: dict with user information
                  (keys are the same as User model columns)
        """
        # extract the username from `userinfo`
        if "username" in userinfo:
            username = userinfo["username"]
        elif "email" in userinfo:
            username = userinfo["email"]
        else:
            log.error("OAUTH userinfo does not have username or email %s", userinfo)
            return None

        # If username is empty, go away
        if (username is None) or username == "":
            return None

        # Search the DB for this user
        user = self.find_user(username=username)

        # If user is not active, go away
        if user and (not user.is_active):
            return None

        # If user is not registered, and not self-registration, go away
        if (not user) and (not self.auth_user_registration):
            return None

        # Sync the user's roles
        if user and self.auth_roles_sync_at_login:
            user.roles = self._oauth_calculate_user_roles(userinfo)
            log.debug("Calculated new roles for user='%s' as: %s", username, user.roles)

        # If the user is new, register them
        if (not user) and self.auth_user_registration:
            user = self.add_user(
                username=username,
                first_name=userinfo.get("first_name", ""),
                last_name=userinfo.get("last_name", ""),
                email=userinfo.get("email", "") or f"{username}@email.notfound",
                role=self._oauth_calculate_user_roles(userinfo),
            )
            log.debug("New user registered: %s", user)

            # If user registration failed, go away
            if not user:
                log.error("Error creating a new OAuth user %s", username)
                return None

        log.debug(f"headquarter {userinfo['headquarter']}")

        # Set tenant_id
        if "headquarter" in userinfo:
            user.headquarter = userinfo["headquarter"]

        # LOGIN SUCCESS (only if user is now registered)
        if user:
            self.update_user_auth_stat(user)
            return user
        else:
            return None

from flask import g

def current_headquarter():
  ids = g.user.headquarter
  print(ids)
  if ids is None:
    return "'-1'"
  ids_list = ids.split(',')
  quoted_ids = [f"'{id_.strip()}'" for id_ in ids_list]
  quoted_ids_str = ','.join(quoted_ids)

  return quoted_ids_str

JINJA_CONTEXT_ADDONS = {
    'current_headquarter': current_headquarter
}
CUSTOM_SECURITY_MANAGER = CustomSecurityManager
FEATURE_FLAGS = { "ENABLE_TEMPLATE_PROCESSING": True,
                  "SQL_VALIDATORS_BY_ENGINE": True,
                  "DASHBOARD_RBAC": True,
                  }

# Setting timezone to UTC
os.environ['TZ'] = 'UTC'

# Default language FR
BABEL_DEFAULT_LOCALE = 'fr'


# secret
# Generate your own secret key for encryption. Use `openssl rand -base64 42` to generate a good key
SECRET_KEY = 'LxJgSoFfVfMbV/nPsLUhvypoK2FeSFCIt8EplizyhU2/YcBWICAHIO19'
