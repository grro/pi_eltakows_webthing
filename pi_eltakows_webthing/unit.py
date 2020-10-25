import pathlib
from os import system, remove
from string import Template

UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --hostname $hostname --port $port --gpio $gpio_number
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')


def register(packagename: str, entrypoint: str, hostname: str, port: int, gpio_number: int):
    unit = UNIT_TEMPLATE.substitute(packagename=packagename, entrypoint=entrypoint, hostname=hostname, port=port, gpio_number=gpio_number)
    service = packagename + "_" + str(port) + ".service"
    unit_file_fullname = str(pathlib.Path("/", "etc", "systemd", "system", service))
    with open(unit_file_fullname, "w") as file:
        file.write(unit)
    system("sudo systemctl daemon-reload")
    system("sudo systemctl enable " + service)
    system("sudo systemctl restart " + service)
    system("sudo systemctl status " + service)


def deregister(packagename, port):
    print("deregister " + packagename + " on port " + str(port))

    service = packagename + "_" + str(port) + ".service"
    unit_file_fullname = str(pathlib.Path("/", "etc", "systemd", "system", service))
    system("sudo systemctl stop " + service)
    system("sudo systemctl disable " + service)
    system("sudo systemctl daemon-reload")
    try:
        remove(unit_file_fullname)
    except Exception as e:
        pass

def printlog(packagename, port):
    service = packagename + "_" + str(port) + ".service"
    system("sudo journalctl -f -u " + service)
