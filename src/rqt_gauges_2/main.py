import sys

from rqt_gui.main import Main
from rqt_gauges_2.speedometer import Speedometer


def main():
    plugin = 'rqt_gauges_2.gauges_2.Speedometer'
    main = Main(filename=plugin)
    sys.exit(main.main(sys.argv, standalone=plugin))


if __name__ == '__main__':
    main()
