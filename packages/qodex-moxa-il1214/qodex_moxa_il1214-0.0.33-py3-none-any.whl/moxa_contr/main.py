import json
import time
import requests


class MoxaServer:
    schema = "http://"
    api_io = f"/api/slot/0/io"
    api_io_di = f"/api/slot/0/io/di"
    headers = {
        "Content-Type": "application/json",
        "Accept": "vdn.dac.v1"
    }

    def __init__(self, ip):
        self.ip = ip

    def get_info(self, route):
        return requests.get(url=f"{self.schema}{self.ip}{route}",
                            headers=self.headers)

    def put_info(self, route, data=None):
        data = json.dumps(data)
        print(f"{self.schema}{self.ip}{route}")
        return requests.put(url=f"{self.schema}{self.ip}{route}",
                            headers=self.headers,
                            data=data)

    def get_di_slot_info(self):
        return self.get_info("/api/slot/0/io/di")

    def start_di_slots_trace_cycle(self):
        while True:
            res = self.get_di_slot_info().json()
            dis = res['io']['di']
            for di in dis:
                if di['diStatus']:
                    print(di)
            time.sleep(0.5)


class MoxaDevice(MoxaServer):
    index = None
    ip = None
    status_on = 1
    status_off = 0

    def __init__(self, ip, index, status_on=1, status_off=0):
        super().__init__(ip=ip)
        self.index = index
        self.status_on = status_on
        self.status_off = status_off
        self.api_relay = f"{MoxaServer.api_io}/relay/{index}"
        self.relay_status_link = f"{self.api_relay}/relayStatus"

    def set_relay_link(self, index):
        self.api_relay = f"{MoxaServer.api_io}/relay/{index}"
        self.relay_status_link = f"{self.api_relay}/relayStatus"

    def get_relay_info(self):
        return self.get_info(self.relay_status_link)

    def get_di_status(self):
        return self.get_info(f"{self.api_io_di}/{self.index}/diStatus")

    def change_relay_status(self, status):
        info = {
            "slot": "0",
            "io": {"relay": {f"{self.index}": {"relayStatus": f"{status}"}}}
        }
        return self.put_info(
            route=self.relay_status_link,
            data=info)

    def set_status_on(self):
        return self.change_relay_status(self.status_on)

    def set_status_off(self):
        return self.change_relay_status(self.status_off)


if __name__ == "__main__":
    ext_gate = MoxaDevice("192.168.60.103", 0)
    int_gate = MoxaDevice("192.168.60.103", 1)
    print(ext_gate.get_di_status().json())
    ext_gate.change_relay_status(1)
    time.sleep(1)
    ext_gate.change_relay_status(0)
    time.sleep(1)
    """
    ext_gate.change_relay_status(1)
    int_gate.change_relay_status(1)
    time.sleep(1)
    int_gate.change_relay_status(0)
    time.sleep(0.5)
    ext_gate.change_relay_status(0)
    time.sleep(1)
    ext_gate.change_relay_status(1)
    int_gate.change_relay_status(1)
    time.sleep(1)
    ext_gate.change_relay_status(0)
    int_gate.change_relay_status(0)
    """
