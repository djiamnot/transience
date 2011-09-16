"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from distutils.core import setup
import py2app
import transience

APP = ['scripts/transienceScore.py']
OPTIONS = {'argv_emulation': True,
           #'iconfile': 'icon.icns' # icon files shall be 'icns' type
} 

setup(
    app=APP,
    name = "Transience",
    version = transience.__version__, 
    author = "Michal Seta",
    author_email = "mis@artengine.ca",
    url = "http://matralab.hexagram.ca",
    description = "Transience Interactive Score",
    long_description = """Transience, a composition by Sandeep Bhagwati, Interactive Score""",
    install_requires = [], # "twisted", "wxpython", "docutils",
    license = "GPL",
    platforms = ["any"],
    zip_safe = True,
    packages = ["transience", "media"],
    package_data = {
        "":["*.cfg", "*.png", "*.jpg", "*.json", "*.txt", "*.rst", ".pdf"]
    },
    #package_dir = {'': 'transience','':'media'},
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],  
)

