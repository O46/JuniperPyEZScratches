from jnpr.junos import Device
from jnpr.junos.utils.config import Config


class BasicSetup:
    """Configures a JunOS device with two interfaces using OSPF"""

    def __init__(self, host: str, username: str, password: str, interfaces: list):
        # Connect to the Junos device
        device = Device(host=host, user = username, password = password)
        device.open()

        # Creates list of interfaces to iterate through
        self.interfaces = interfaces

        # Create a configuration object
        self.cu = Config(device)

    def set_hostname(self, host_name):
        # Set the hostname
        self.cu.load(f"set system host - name {host_name}", format = "set")
        self.cu.commit()

    def conf_interfaces(self):
        # Configure the interfaces
        if not self.interfaces:
            self.interfaces = [
                {'name': 'ge-0/0/0', 'ip': '10.0.0.1/24'},
                {'name': 'ge-0/0/1', 'ip': '10.0.1.1/24'},
            ]
        for interface in self.interfaces:
            self.cu.load(f"set interfaces {interface['name']} unit 0 family inet address {interface['ip']}",
                         format="set")
            self.cu.commit()

    def conf_ospf(self):
        # Configure OSPF
        self.cu.load(f"""
        set protocols ospf area 0.0.0.0 {"set protocols ospf interface ".join(interface) for interface in self.interfaces}
        set protocols ospf passive-interface lo0.0"
        """, format="set")
        self.cu.commit()

def dev_disconnect(self):
    # Disconnect from the device
    self.device.close()


if __name__ == "__main__":
    device_setup = BasicSetup("testhost", "admin", "pass", [{"name": "ge-0/0/0", "ip":"10.0.0.1/24"},
                                                            {"name": "ge-0/0/1", "ip": "10.0.1.1/24"}])
    device_setup.set_hostname("nameOfHostDevice")
    device_setup.conf_interfaces()
    device_setup.conf_ospf()
    device_setup.dev_discconect()
