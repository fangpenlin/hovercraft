from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.0.0'
try:
    import gf_player
    version = gf_player.__version__
except ImportError:
    pass

tests_require = [
    'nose',
    'nose-cov',
    'mock',
    'webtest',
]

setup(
    name='hovercraft',
    version=version,
    packages=find_packages(),
    install_requires=[
        'waitress',
        'pyramid_tm',
        'pyramid_debugtoolbar',
        'boto',
        'Pyramid',
        'SQLAlchemy',
        'zope.sqlalchemy',
        'transaction',
        'click',
        'pytz',
        'wtforms',
        'venusian',
    ],
    extras_require=dict(
        tests=tests_require,
    ),
    tests_require=tests_require,
    entry_points="""\
    [console_scripts]
    hovercraft = hovercraft.scripts.__main__:main
    hc = hovercraft.scripts.__main__:main
    """,
)
