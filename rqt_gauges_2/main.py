import sys

from rqt_gui.main import Main
from rqt_gauges_2.gauges_2 import Gauges2


def main():
    plugin = 'rqt_gauges_2.gauges_2.Gauges2'
    main = Main(filename=plugin)
    sys.exit(main.main(standalone=plugin, plugin_argument_provider=Gauges2.add_arguments))


if __name__ == '__main__':
    main()