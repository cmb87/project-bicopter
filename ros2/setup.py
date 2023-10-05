import os
from glob import glob
from setuptools import setup
from setuptools import find_packages



package_name = 'drone_model'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.py')),
        (os.path.join('share', package_name, "urdf"), glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='christian.peeren@rwth-aachen.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           'propeller = drone_model.propeller:main',
           'propellerSingle = drone_model.propellerSingle:main',
           'controller = drone_model.controller:main',
        ],
    },
)
