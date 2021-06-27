"""Time utils for getting and converting datetime objects for the Mycroft
system. This time is based on the setting in the Mycroft config and may or
may not match the system locale.
"""
from datetime import datetime
from dateutil.tz import gettz, tzlocal
from mycroft.util.log import LOG

# we want to support both LF and LN
# when using the mycroft wrappers this is not an issue, but skills might use
# either, so mycroft-lib needs to account for this and set the defaults for
# both libs.
# if neither LF or LN are installed provide dummy methods
# exceptions should be raised in the actual functionality,
# not on loading of core itself

try:
    import lingua_franca as LF
except ImportError:
    LF = None

try:
    import lingua_nostra as LN
except ImportError:
    LN = None

try:
    try:
        from lingua_nostra.time import now_utc, now_local, to_local, to_utc
    except ImportError:
        from lingua_franca.time import now_utc, now_local, to_local, to_utc
except ImportError:
    # lingua_franca/lingua_nostra are optional and should not be needed
    # because of time utils, only parse and format utils require it

    # TODO improve this, duplicating code is usually bad

    def now_utc():
        return to_utc(datetime.utcnow())


    def now_local(tz=None):
        tz = tz or default_timezone()
        return datetime.now(tz)


    def to_utc(dt):
        tz = gettz("UTC")
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=default_timezone())
        return dt.astimezone(tz)


    def to_local(dt):
        tz = default_timezone()
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=default_timezone())
        return dt.astimezone(tz)


def set_default_tz(tz=None):
    """ configure both LF and LN """
    if LN:
        LN.time.set_default_tz(tz)
    if LF:
        # tz added in recently, depends on version
        try:
            LF.time.set_default_tz(tz)
        except:
            if not LN:
                LOG.warning("mycroft-lib is using lingua_franca, it does not handle "
                            "timezones correctly, check for new releases or "
                            "install lingua_nostra instead")
                LOG.error("pip install lingua_nostra")


def default_timezone():
    """Get the default timezone

    Based on user location settings location.timezone.code or
    the default system value if no setting exists.

    Returns:
        (datetime.tzinfo): Definition of the default timezone
    """
    try:
        # Obtain from user's configured settings
        #   location.timezone.code (e.g. "America/Chicago")
        #   location.timezone.name (e.g. "Central Standard Time")
        #   location.timezone.offset (e.g. -21600000)
        from mycroft.configuration import Configuration
        config = Configuration.get()
        code = config["location"]["timezone"]["code"]
        return gettz(code)
    except Exception:
        # Just go with LF/LN default timezone
        if LN:
            return LN.time.default_timezone()
        if LF:
            return LF.time.default_timezone()
        # Just go with system default timezone
        return tzlocal()


def to_system(dt):
    """Convert a datetime to the system's local timezone

    Arguments:
        dt (datetime): A datetime (if no timezone, assumed to be UTC)
    Returns:
        (datetime): time converted to the operation system's timezone
    """
    tz = tzlocal()
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=default_timezone())
    return dt.astimezone(tz)
