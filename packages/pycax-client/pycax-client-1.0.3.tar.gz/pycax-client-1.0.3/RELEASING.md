# Release process

_This is only of interest to the project maintainers._

See https://github.com/gbif/pygbif/blob/master/RELEASING.md for a version with testpypi and preparing a release via terminal (locally) rather than via a GitHub Action.

0. Prepare PyPi -- this is already completed

   - Create and account
   - Create a project link to GitHub
   - Create an API token
   - Create an organizational secret called PYPI_API_TOKEN and make available to repository with the Python package
   

1. Test the package

    After making changes, reinstall using the following code. This assumes you are running this code from the base of your Python package.

    ```
    # install from source (base dir)
    python3 -m pip install -e .
    # test your installation
    python3 -m pytest
    # test and generate a coverage report
    python3 -m pytest -rxs --cov=pycax --cov-report term-missing ./pycax
    # make the documentation in docs/_build/html
    cd docs # pycax/docs
    make clean html codecov # linkcheck # linkcheck is currently not working
    ```

2. Prepare the release

    Update `Changelog.rst` with a new section describing the changes in this release

3. Create a release on GitHub

    Go to https://github.com/nwfsc-math-bio/pycax/releases and create a release.

4. Upload to PyPi

    This is handled by the GitHub Action `.github/workflows/pypi.yml` and is triggered by a release created on GitHub. The version number will become the version of the release.


