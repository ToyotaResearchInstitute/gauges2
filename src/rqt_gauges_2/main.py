import sys

from rqt_gui.main import Main


def main():
    main = Main()
    sys.exit(main.main(sys.argv, standalone='rqt_gauges_2.gauges_2.Gauges2'))


if __name__ == '__main__':
    main()