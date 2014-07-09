from os import path

from setuptools import setup


def get_readme_text():
    readme_path = path.abspath(path.join(__file__, "../README.rst"))
    with open(readme_path) as readme:
        return readme.read()

def get_version(filename):
    """
    Parse the value of the __version__ var from a Python source file
    without running/importing the file.
    """
    import re
    version_pattern = r"^ *__version__ *= *['\"](\d+\.\d+\.\d+)['\"] *$"
    match = re.search(version_pattern, open(filename).read(), re.MULTILINE)

    assert match, ("No version found in file: {!r} matching pattern: {!r}"
                   .format(filename, version_pattern))

    return match.group(1)


setup(
    name="django-cam-auth-utils",
    version=get_version("django_cam_auth_utils/__init__.py"),
    description=get_readme_text(),
    author="Hal Blackburn",
    author_email="hwtb2@cam.ac.uk",
    url="https://github.com/ucamhal/django-cam-auth-utils",
    packages=["django_cam_auth_utils"],
    install_requires=[
        "django>=1.5",
        "django-braces"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: BSD License'
    ]
)
