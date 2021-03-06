import psutil

def cpu_info():
    cpu_times = {'cpu_times': dict(psutil.cpu_times()._asdict())}
    cpu_percent = {'cpu_percent': psutil.cpu_percent(percpu=False)}
    cpu_count = {'cpu_count': psutil.cpu_count()}
    
    return {**cpu_times, **cpu_percent, **cpu_count}

def memory_info():
    virtual_mem = {'virtual_mem': dict(psutil.virtual_memory()._asdict())}
    swap = {'swap': dict(psutil.swap_memory()._asdict())}
    
    return {**virtual_mem, **swap}

def disk_info():
    partitions = {'partitions': [dict(item._asdict()) for item in psutil.disk_partitions()]}
    usage = {'usage': dict(psutil.disk_usage('/')._asdict())}
    io = psutil.disk_io_counters(perdisk=True)
    io_counters = {'io_counters': [dict(io[item]._asdict()) for item in io]}
    
    return {**partitions, **usage, **io_counters}

def network_info():
    tmp = psutil.net_io_counters(pernic=True)
    net_io = {'net_io': [dict(tmp[item]._asdict()) for item in tmp]}
    net_if = {'net_if': psutil.net_if_addrs()}
    
    return {**net_io, **net_if}

def sensor_info():
    try: 
        tmp = psutil.sensors_temperatures()
        temps = {'temps': [[dict(t._asdict()) for t in tmp[item]] for item in tmp]}
        tmp = psutil.sensors_fans()
        fans = {'fans': [[dict(t._asdict()) for t in tmp[item]] for item in tmp]}
        battery = {'battery': dict(psutil.sensors_battery()._asdict())}
        
        return {**temps, **fans, **battery, 'status': 'SUCCESS'}
    except:
        return { 'status': 'FAILED' }
        

def user_info():
    u = psutil.users()
    return {'users': [dict(item._asdict()) for item in u]}

def return_all_info():
    cpu = {'cpu': cpu_info()}
    mem = {'memory': memory_info()}
    dsk = {'disk': disk_info()}
    net = {'network': network_info()}
    sen = {'sensors': sensor_info()}
    usr = {'users': user_info()}
    
    return {**cpu, **mem, **dsk, **net, **sen, **usr}

if __name__ == '__main__':
    print(return_all_info())
