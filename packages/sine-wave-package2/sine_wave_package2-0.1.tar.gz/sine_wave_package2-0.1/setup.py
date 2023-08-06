from setuptools import setup, find_packages
print('find packages: ', find_packages())
setup(
    name='sine_wave_package2',
    version='0.1',
    description='A package that creates a sine wave',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'sine_wave=sine_wave.sine_wave:main',
        ],
    },
)
