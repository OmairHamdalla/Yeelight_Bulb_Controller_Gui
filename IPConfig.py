import json
import os
import time
from yeelight import Bulb, BulbException
import socket

class IPFinder:
    def __init__(self, config_file='config.json', ip_range='192.168.1.', start=2, end=254, debug=False):
        self.config_file = config_file
        self.ip_range = ip_range
        self.start = start
        self.end = end
        self.bulb_ip = None
        self.debug = debug

    # To only print if debug mode is on. (VERY USEFUL)
    def _log(self, message):
        if self.debug:
            print("[DEBUG]", message)

    ## Checks for the last saved ip if it works to load it
    def _load_saved_ip(self):
        self._log("Checking for saved IP in config file. ")
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    saved_ip = data.get("bulb_ip", None)
                    self._log(f"Found saved IP: {saved_ip}")
                    return saved_ip
            except Exception as e:
                self._log(f"Error reading config file: {e}")
        else:
            self._log("No config file found.")
        return None
    
    ## Saves the ip for next use
    def _save_ip(self, ip):  
        self._log(f"Saving working IP to config: {ip}")
        try:
            with open(self.config_file, 'w') as f:
                json.dump({"bulb_ip": ip}, f)
        except Exception as e:
            self._log(f"Error writing config : {e}")

    # Try to ping the bulb with a yeelight function
    def _is_bulb_alive(self, ip):
        self._log(f"Trying IP: {ip}")
        try:
            bulb = Bulb(ip, effect="smooth", duration=100)
            bulb.get_properties()
            self._log(f"Successsssss: Yeelight bulb responded at {ip}")
            return True
        except (BulbException, socket.error) as e:
            self._log(f"Failed: No response from {ip}")
            return False

    def discover_bulb(self):
        self._log("Starting bulb discovery!!!")
        start_time = time.time() if self.debug else None

        # Step 1: Try saved IP
        saved_ip = self._load_saved_ip()
        if saved_ip and self._is_bulb_alive(saved_ip):
            self.bulb_ip = saved_ip
            self._log(f"Using saved IP: {saved_ip}")
            if self.debug:
                elapsed = time.time() - start_time
                self._log(f"Discovery complete in {elapsed:.2f} seconds.")
            return saved_ip

        # Step 2: Scan range
        self._log(f"Scanning IP from {self.ip_range}{self.start} to {self.ip_range}{self.end}...")
        for i in range(self.start, self.end + 1):
            ip = f"{self.ip_range}{i}"
            if self._is_bulb_alive(ip):
                self.bulb_ip = ip
                self._save_ip(ip)
                if self.debug:
                    elapsed = time.time() - start_time
                    self._log(f"Discovery complete in {elapsed:.2f} seconds.")
                return ip

        self._log("Bulb not found on network.")
        if self.debug:
            elapsed = time.time() - start_time
            self._log(f"Discovery finished in {elapsed:.2f} seconds with no result.")
        return None

    def get_bulb_ip(self):
        if not self.bulb_ip:
            self.discover_bulb()
        return self.bulb_ip

    def print_bulb_ip(self):
        ip = self.get_bulb_ip()
        if ip:
            print(f"Yeelight bulb IP set at: {ip}")
        else:
            print("Yeelight bulb not found.....")


if __name__ == "__main__":
    finder = IPFinder(debug=True)
    finder.print_bulb_ip()
