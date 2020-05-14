"""
_compat module (imdb package).
"""

# TODO: now we're heavily using the 'logging' module, which was not
#       present in Python 2.2.  To work in a Symbian environment, we
#       need to create a fake 'logging' module (its functions may call
#       the 'warnings' module, or do nothing at all).


import os
# If true, we're working on a Symbian device.
if os.name == 'e32':
    # Replace os.path.expandvars and os.path.expanduser, if needed.
    def _noact(x):
        """Ad-hoc replacement for media_browser."""
        return x
    try:
        os.path.expandvars
    except AttributeError:
        os.path.expandvars = _noact
    try:
        os.path.expanduser
    except AttributeError:
        os.path.expanduser = _noact

    # time.strptime is missing, on Symbian devices.
    import time
    try:
        time.strptime
    except AttributeError:
        import re
        _re_web_time = re.compile(r'Episode dated (\d+) (\w+) (\d+)')
        _re_ptdf_time = re.compile(r'\((\d+)-(\d+)-(\d+)\)')
        _month2digit = {'January': '1', 'February': '2', 'March': '3',
                'April': '4', 'May': '5', 'June': '6', 'July': '7',
                'August': '8', 'September': '9', 'October': '10',
                'November': '11', 'December': '12'}
        def strptime(s, format):
            """Ad-hoc strptime replacement for media_browser."""
            try:
                if format.startswith('Episode'):
                    res = _re_web_time.findall(s)[0]
                    return (int(res[2]), int(_month2digit[res[1]]), int(res[0]),
                            0, 0, 0, 0, 1, 0)
                else:
                    res = _re_ptdf_time.findall(s)[0]
                    return (int(res[0]), int(res[1]), int(res[2]),
                            0, 0, 0, 0, 1, 0)
            except:
                raise ValueError('error in media_browser\'s ad-hoc strptime!')
        time.strptime = strptime

