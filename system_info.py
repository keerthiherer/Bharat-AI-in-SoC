import psutil, socket, datetime

def time_now(): return datetime.datetime.now().strftime("%H:%M:%S")
def date_today(): return datetime.date.today().strftime("%d %B %Y")
def day_today(): return datetime.datetime.now().strftime("%A")
def uptime(): return str(datetime.datetime.now() -
                        datetime.datetime.fromtimestamp(psutil.boot_time())).split('.')[0]
def cpu(): return f"{psutil.cpu_percent()} %"
def ram(): return f"{psutil.virtual_memory().percent} %"
def disk(): return f"{psutil.disk_usage('/').percent} %"
def battery():
    b = psutil.sensors_battery()
    return f"{b.percent} %" if b else "उपलब्ध नहीं"
def temp():
    try:
        return f"{list(psutil.sensors_temperatures().values())[0][0].current} °C"
    except:
        return "उपलब्ध नहीं"
def network():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return "इंटरनेट चालू है"
    except:
        return "इंटरनेट बंद है"
def ip(): return socket.gethostbyname(socket.gethostname())
def hostname(): return socket.gethostname()

