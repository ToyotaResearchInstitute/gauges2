from setuptools import setup

package_name = 'rqt_gauges_2'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/resource',
            ['resource/gauges_2_widget.ui']),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugin.xml']),
    ],
    install_requires=['setuptools'],
    maintainer='Eloy Briceno',
    maintainer_email='eloy.briceno@ekumenlabs.com',
    description=(
        'rqt_gauges_2 is a Python GUI plugin providing a visualization tool for several sensors.'
    ),
    entry_points={
        'console_scripts': [
            'rqt_gauges_2 = ' + package_name + '.main:main',
        ],
    },
)
