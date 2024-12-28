import psutil
import time

def monitor_bandwidth(duration=10):
    start_counters = psutil.net_io_counters()
    time.sleep(duration)
    end_counters = psutil.net_io_counters()

    bytes_sent = end_counters.bytes_sent - start_counters.bytes_sent
    bytes_recv = end_counters.bytes_recv - start_counters.bytes_recv

    print(f"Data sent: {bytes_sent / 1024:.2f} KB")
    print(f"Data received: {bytes_recv / 1024:.2f} KB")

monitor_bandwidth(60)  # Giám sát trong 60 giây
