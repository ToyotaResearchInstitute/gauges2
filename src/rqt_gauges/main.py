import sys

from rqt_gui.main import Main


def main():
    plugin = 'rqt_gauges.dial.Dial'
    main = Main(filename=plugin)
    sys.exit(main.main(sys.argv, standalone=plugin))


if __name__ == '__main__':
    main()
