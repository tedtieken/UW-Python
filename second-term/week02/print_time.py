import time
import datetime

output = \
"""<html>
<head><title>Time! %s</title></head>
<body>
Here is the time: %s<br />
and again: %s
</body>
</html>
"""

print output % (time.time(), time.time(), datetime.datetime.now())