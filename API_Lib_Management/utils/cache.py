# currently we use app.cache directly; this file can hold helpers like cache_key builders
def make_cache_key(*parts):
    return ":".join(str(p) for p in parts)
