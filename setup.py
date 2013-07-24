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
    author_email="hal@caret.cam.ac.uk",
    packages=["django_cam_auth_utils"],
    zip_safe=False,
    install_requires=[
        "django>=1.5",
        "django-braces"
    ]
)
