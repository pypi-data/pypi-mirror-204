from setuptools import setup, find_packages
# import codecs
# import os
# 
# here = os.path.abspath(os.path.dirname(__file__))
# 
# with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Adds Python functions/methods to the Windows context menu'''

# Setting up
setup(
    name="shellextools",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/shellextools',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['amiadmin', 'ctypestoast', 'downloadunzip', 'escape_windows_filepath', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'isiter', 'list_all_files_recursively', 'list_files_with_timestats', 'reggisearch', 'subprocess_alive', 'subprocesskiller', 'tolerant_isinstance', 'touchtouch'],
    keywords=['Windows context menu', 'python', 'nutika'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['amiadmin', 'ctypestoast', 'downloadunzip', 'escape_windows_filepath', 'flatten_any_dict_iterable_or_whatsoever', 'flatten_everything', 'isiter', 'list_all_files_recursively', 'list_files_with_timestats', 'reggisearch', 'subprocess_alive', 'subprocesskiller', 'tolerant_isinstance', 'touchtouch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*