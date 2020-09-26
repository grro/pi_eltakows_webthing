import pathlib
from os import system, remove
from string import Template
import pi_eltakows_webthing.settings as SETTINGS


UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --port $port --gpio $gpio_number
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')


def register(port, gpio_number):
    unit = UNIT_TEMPLATE.substitute(packagename=SETTINGS.PACKAGENAME, entrypoint=SETTINGS.ENTRY_POINT, port=port, gpio_number=gpio_number)
    service = SETTINGS.PACKAGENAME + "_" + str(port) + ".service"
    unit_file_fullname = str(pathlib.Path("/", "etc", "systemd", "system", service))
    with open(unit_file_fullname, "w") as file:
        file.write(unit)
    system("sudo systemctl daemon-reload")
    system("sudo systemctl enable " + service)
    system("sudo systemctl restart " + service)
    system("sudo systemctl status " + service)


def deregister(port):
    print("deregister " + SETTINGS.PACKAGENAME + " on port " + str(port))

    service = SETTINGS.PACKAGENAME + "_" + str(port) + ".service"
    unit_file_fullname = str(pathlib.Path("/", "etc", "systemd", "system", service))
    system("sudo systemctl stop " + service)
    system("sudo systemctl disable " + service)
    system("sudo systemctl daemon-reload")
    try:
        remove(unit_file_fullname)
    except Exception as e:
        pass

