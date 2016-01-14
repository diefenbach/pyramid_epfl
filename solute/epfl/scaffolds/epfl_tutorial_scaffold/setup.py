import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_beaker',
    'pyramid_jinja2',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'wtforms',
    'ujson',
    ]

setup(name='epfl_tutorial',
      version='0.0',
      description='epfl_tutorial',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="epfl_tutorial",
      entry_points="""\
      [paste.app_factory]
      main = epfl_tutorial:main
      """,
      )
