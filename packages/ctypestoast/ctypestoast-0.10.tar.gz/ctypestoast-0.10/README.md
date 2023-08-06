# Toast notification for Windows - ctypes only - no dependency

## pip install ctypestoast



```python
	
from ctypestoast import show_notification,show_notification_threaded
show_notification(
    title="work done",
    msg="i am ready",
    icon_path=r"C:\Users\hansc\Downloads\1.ico",
    repeat=3,
    sleeptime=1,
)
show_notification_threaded(
    title="work done",
    msg="i am ready",
    icon_path=r"C:\Users\hansc\Downloads\1.ico",
    repeat=3,
    sleeptime=1,
)

```