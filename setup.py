import subprocess

from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)


class build_ext(_build_ext, object):
    def run(self):
        _run("make", "LKH-2.0.9")

        super(build_ext, self).run()


setup(
    name='pypopmusic',
    author='Tommaso Vitali',
    author_email='tommivitali@gmail.com',
    url='https://github.com/tommivitali/pypopmusic',
    description='Python wrapper around the POPMusic TSP solver',
    install_requires=[
        'numpy',
    ],
    cmdclass={
        'build_ext': build_ext,
    }
)