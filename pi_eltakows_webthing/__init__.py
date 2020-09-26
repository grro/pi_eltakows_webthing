import argparse
import pi_eltakows_webthing.settings as SETTINGS
from pi_eltakows_webthing.eltako_webthing import run_server
from pi_eltakows_webthing.unit import register, deregister


def main():
    parser = argparse.ArgumentParser(description=SETTINGS.DESCRIPTION)
    parser.add_argument('--command', metavar='command', required=True, type=str, help='the command. Supported commands are: listen (run the webthing service), register (register and starts the webthing service as a systemd unit, deregister (deregisters the systemd unit')
    parser.add_argument('--port', metavar='port', required=True, type=int, help='the port of the webthing serivce')
    parser.add_argument('--gpio', metavar='gpio', required=False, type=int, help='the gpio number wired to the device')
    args = parser.parse_args()

    if args.command == 'listen':
        print("running " + SETTINGS.PACKAGENAME + " on port " + str(args.port) + "/gpio " + str(args.gpio))
        run_server(int(args.port), int(args.gpio))
    elif args.command == 'register':
        print("register " + SETTINGS.PACKAGENAME + " on port " + str(args.port) + "/gpio " + str(args.gpio) + " and starting it")
        register(int(args.port), int(args.gpio))
    elif args.command == 'deregister':
        deregister(int(args.port))
    else:
        print("usage " + SETTINGS.ENTRY_POINT + " --help")


if __name__ == '__main__':
    main()

