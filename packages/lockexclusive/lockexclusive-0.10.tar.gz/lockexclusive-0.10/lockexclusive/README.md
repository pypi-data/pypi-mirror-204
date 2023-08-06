# Limits the number of running instances of a Python script

## pip install lockexclusive 

## How to use it

```python
import sys
from time import sleep

from lockexclusive import configure_lock

# it can be used like this:
# configure_lock(maxinstances=1, message="More than one instance running",file=sys.argv[0])

# or without the file argument:
configure_lock(maxinstances=1, message="More than one instance running")

sleep(100)


```

