try:
    from .settings_prod import *
except ModuleNotFoundError:
    from .settings_dev import *
    try:
        from .settings_local import *
    except ModuleNotFoundError:
        pass
