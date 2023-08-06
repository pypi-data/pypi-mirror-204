"""
Documentar.
"""

import dynaconf
from rds_core.config import settings
from rds_core.helpers import instantiate_class


caches = {}

if 'CACHES' in settings and isinstance(settings.CACHES, dynaconf.utils.boxing.DynaBox):
    for cache_name, cache_configs in settings.CACHES.items():
        caches[cache_name] = instantiate_class(cache_configs['BACKEND'], **cache_configs.get('OPTIONS', {}))
    default_cache = caches.get('default', instantiate_class('rds_core.cache.nocache.NoCache'))
else:
    default_cache = instantiate_class('rds_core.cache.nocache.NoCache')
