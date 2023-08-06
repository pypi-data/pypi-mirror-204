from pathlib import Path

from setuptools import setup

test_deps = [
    'pytest', 
    'pytest-runner', 
    'pytest-cov', 
    'vcrpy', 
    'pytest-vcr', 
    'pytest-mock', 
    'requests-mock',
    'pytz'
]

webpush_deps = [
    'http_ece>=1.0.5',
    'cryptography>=1.6.0',
]

blurhash_deps = [
    'blurhash>=1.1.4',
]

extras = {
    "test": test_deps + webpush_deps + blurhash_deps,
    "webpush": webpush_deps,
    "blurhash": blurhash_deps,
}

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(name='Mastodon.py',
      version='1.8.1',
      description='Python wrapper for the Mastodon API',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      packages=['mastodon'],
      install_requires=[
          'requests>=2.4.2', 
          'python-dateutil', 
          'six',
          'python-magic-bin ; platform_system=="Windows"', # pragma: no cover
          'python-magic ; platform_system!="Windows"',
          'decorator>=4.0.0', 
      ] + blurhash_deps,
      tests_require=test_deps,
      extras_require=extras,
      url='https://github.com/halcy/Mastodon.py',
      author='Lorenz Diener',
      author_email='lorenzd+mastodonpypypi@gmail.com',
      license='MIT',
      keywords='mastodon api microblogging',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Communications',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ])
