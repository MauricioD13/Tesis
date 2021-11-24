import wifi_class


if __name__ == '__main__':
    airmon = wifi_class.Airmon()
    airodump = wifi_class.Airodump()
    
    airmon.get_interface()
    airmon.monitor_mode()
    
    airodump.scan_targets(airmon.monitor_interface)