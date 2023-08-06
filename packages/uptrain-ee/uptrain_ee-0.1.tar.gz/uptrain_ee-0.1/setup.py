from setuptools import setup

setup(
    name='uptrain_ee',
    version='0.1',
    packages=['uptrain_ee_compiled'],
    package_data={'uptrain_ee_compiled': ['__pycache__/*.pyc']},
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)