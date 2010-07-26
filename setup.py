"""
Script for building the example.

Usage:
    python setup.py py2app
"""
from distutils.core import setup
import py2app

NAME = 'Subterranean'
VERSION = '0.1'

plist = dict(
    CFBundleIconFile='English.lproj/Subterranean.icns',
    CFBundleName=NAME,
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
    CFBundleIdentifier='org.subterranean',
)

setup(
data_files=['English.lproj', 'Assets','Libraries','Resources'],
    app=[
        dict(script="main.py", plist=plist),
    ],
)
