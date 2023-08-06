from setuptools import setup

setup(
    name="odoo_image_changelog",
    version="0.1.0",
    description="a odoo changelog generator",
    url="https://github.com/camptocamp/odoo-image-changelog",
    author="Camptocamp (Vincent Renaville)",
    author_email="vincent.renaville@camptocamp.com",
    packages=["odoo_image_changelog"],
    install_requires=[
        "PyGithub",
        "ruamel.yaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "generate_changelog=" "odoo_image_changelog.main:main",
        ]
    },
)
