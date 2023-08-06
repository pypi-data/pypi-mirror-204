import ctypes
from ctypes import wintypes
from time import sleep
import threading
NIF_ICON = 0x00000002
NIF_MESSAGE = 0x00000001
NIF_INFO = 0x00000010
NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
WM_USER = 0x0400
LR_LOADFROMFILE = 0x00000010
LR_CREATEDIBSECTION = 0x00002000

WM_ICON_NOTIFY = WM_USER + 1

class NOTIFYICONDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("hWnd", ctypes.c_void_p),
        ("uID", ctypes.c_uint),
        ("uFlags", ctypes.c_uint),
        ("uCallbackMessage", ctypes.c_uint),
        ("hIcon", ctypes.c_void_p),
        ("szTip", ctypes.c_wchar * 128),
        ("dwState", ctypes.c_uint),
        ("dwStateMask", ctypes.c_uint),
        ("szInfo", ctypes.c_wchar * 256),
        ("uTimeout", ctypes.c_uint),
        ("szInfoTitle", ctypes.c_wchar * 64),
        ("dwInfoFlags", ctypes.c_uint),
    ]


def load_icon(
    icon_path,
    icon_type=1,
    cx_desired=32,
    cy_desired=32,
    load_flags=LR_LOADFROMFILE | LR_CREATEDIBSECTION,
):
    user32 = ctypes.windll.user32
    LoadImage = user32.LoadImageW
    LoadImage.restype = (
        ctypes.c_void_p
    )
    LoadImage.argtypes = [
        wintypes.HINSTANCE,
        wintypes.LPCWSTR,
        wintypes.UINT,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    ]

    icon = LoadImage(None, icon_path, icon_type, cx_desired, cy_desired, load_flags)
    if not icon:
        raise ValueError("Failed to load icon from file")

    return icon


WNDPROC = ctypes.WINFUNCTYPE(
    wintypes.LPARAM, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
)


class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

# def wnd_proc(hwnd, msg, wparam, lparam):
#     # called???
#     #print(msg)
#     if msg == user32.WM_DESTROY:
#         user32.PostQuitMessage(0)
#     return user32.DefWindowProcW(hwnd, msg, wparam, lparam)
def _show_notification(text, title="", icon_path=None, folder_path=None):
    shell32 = ctypes.windll.shell32
    user32 = ctypes.windll.user32
    nid = NOTIFYICONDATA()
    nid.cbSize = ctypes.sizeof(NOTIFYICONDATA)
    nid.hWnd = 0
    nid.uID = 0
    NIF_TIP = 0x00000004
    nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP
    nid.uCallbackMessage = WM_USER + 20
    nid.hIcon = 0
    HWND_MESSAGE = 0xFFFFFFFF
    if icon_path:
        nid.hIcon = load_icon(icon_path)
    nid.szTip = text
    shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid))
    nid.szTip = text
    nid.szInfo = text
    nid.szInfoTitle = title
    nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_INFO
    nid.folder_path = folder_path
    nid.uTimeout = 5000
    nid.uCallbackMessage = WM_ICON_NOTIFY
    shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(nid))
    wc = WNDCLASS()
    wc.lpszClassName = "NotificationHandler"
    user32.RegisterClassW(wc)
    hwnd = user32.CreateWindowExW(
        wc.lpszClassName , "", 0, 0, 0, 0, 0, HWND_MESSAGE, None, None, None
    )

    return hwnd


def show_notification(title="Notification", msg="Here comes the message",
        icon_path=None, repeat=1, sleeptime=1):
    for q in range(repeat):
        _show_notification(msg, title=title, icon_path=icon_path, folder_path=None)
        sleep(sleeptime)


def show_notification_threaded(title="Notification", msg="Here comes the message",
        icon_path=None, repeat=1, sleeptime=1):
    t = threading.Thread(target=show_notification, args=(title,msg,icon_path,repeat,sleeptime))
    t.start()



