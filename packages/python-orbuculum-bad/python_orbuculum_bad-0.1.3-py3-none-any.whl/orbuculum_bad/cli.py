from orbuculum_bad import OrbuculumEtherClient
from subprocess import PIPE, run

def ifconfig():
    """Print ifconfig with replaced contents"""
    client = OrbuculumEtherClient("127.0.0.1:15051")

    interface_mapping = client.get_interface_mapping()
    res = []

    for interface, connection in interface_mapping.items():
        proc = run(["/usr/sbin/ifconfig", interface], stdout=PIPE)
        output = proc.stdout.decode()
        output = output.replace(interface, connection)
        res.append(output.strip())

    print("\n\n".join(res))
