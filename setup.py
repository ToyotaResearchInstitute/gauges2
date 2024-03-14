from setuptools import setup

package_name = 'rqt_gauges'

setup(
    name=package_name,
    version='0.0.3',
    packages=[package_name],
    package_dir={'': 'src'},
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name + '/resource',
            ['resource/dial.ui']),
        ('share/' + package_name + '/resource',
            ['resource/rotational.ui']),
        ('share/' + package_name + '/resource',
            ['resource/bar.ui']),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['plugin.xml']),
    ],
    install_requires=['setuptools'],
    maintainer='Eloy Briceno',
    maintainer_email='eloy.briceno@ekumenlabs.com',
    description=(
        'rqt_gauges is a Python GUI plugin providing a visualization tool for several sensors.'
    ),
    license='BSD Clause 3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_gauges = ' + package_name + '.main:main',
        ],
    },
)
