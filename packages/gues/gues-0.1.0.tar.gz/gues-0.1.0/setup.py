from setuptools import setup


def long_description():
    with open("README.md") as readme:
        return readme.read()


setup(
    name="gues",
    version="0.1.0",
    author="Alex Markham",
    author_email="alex.markham@causal.dev",
    description="This package is for (hybrid and) score-based causal structure learning, using unconditional equivalence classes to reduce the search space.",
    long_description_content_type="text/markdown",
    long_description=long_description(),
    license="GNU Affero General Public License 3 or later (AGPL 3+)",
    packages=["gues"],
    install_requires=["numpy"],
    extras_require={
        "dcor": ["dcor"],
        "ges": ["ges"],
        "all": ["dcor", "ges"],
    },
)
