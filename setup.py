from os import path

from setuptools import setup

def get_readme_text():
    readme_path = path.abspath(path.join(__file__, "../README.rst"))
    with open(readme_path) as readme:
        return readme.read()


setup(
    name="django-cam-auth-utils",
    version="0.0.1",
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
