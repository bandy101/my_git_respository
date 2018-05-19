import pyHook
import pyHook.HookManager
from pyHook import HookManager 
from ctypes import *  
from PIL import ImageGrab
import pythoncom
import win32gui, win32ui, win32con, win32api
user32 = windll.user32  
kernel32 = windll.kernel32  
psapi = windll.psapi  
current_window = None  
num = 0
#   v
def window_capture(filename):
    hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
def get_current_process():  
   
    # 获取最上层的窗口句柄  
    hwnd = user32.GetForegroundWindow()  
    # 获取进程ID  
    pid = c_ulong(0)  
    user32.GetWindowThreadProcessId(hwnd,byref(pid))  
   
    # 将进程ID存入变量中  
    process_id = "%d" % pid.value  
   
    # 申请内存  
    executable = create_string_buffer("\x00"*512)  
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)  
   
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)  
   
    # 读取窗口标题  底层API喊来获取窗口标题
    windows_title = create_string_buffer("\x00"*512)  
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)  
   
    # 打印  
    # print  v
    print ("[ PID:%s-%s-%s]"%(process_id,executable.value,windows_title.value))
    # print  
   
    # 关闭handles  
    kernel32.CloseHandle(hwnd)  
    kernel32.CloseHandle(h_process)  
def onKeyboardEvent(event):
    global current_window  
    global num
    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)  
    if event.WindowName != current_window:  
        current_window = event.WindowName  
        # 函数调用  
        # get_current_process()  
    if event.Key=='V':
        # im = ImageGrab.grab()
        # im.save(str(num)+'.jpg')
        # num +=1
        window_capture('hh.jpg')
    else:pass
    import msvcrt
    print (ord(msvcrt.getch()))
    return True
hm = pyHook.HookManager.HookManager()   
hm.KeyDown = onKeyboardEvent
hm.HookKeyboard() 
pythoncom.PumpMessages() 

if __name__=='__main__':

    import time
    import win32gui, win32ui, win32con, win32api
    hm = pyHook.HookManager.HookManager()
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages() 
    beg = time.time()
    # if 
    # window_capture("haha.jpg")
    # end = time.time()
    # print(end - beg)