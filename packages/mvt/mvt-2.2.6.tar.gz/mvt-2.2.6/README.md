<p align="center">
     <img src="https://docs.mvt.re/en/latest/mvt.png" width="200" />
</p>

# Mobile Verification Toolkit

[![](https://img.shields.io/pypi/v/mvt)](https://pypi.org/project/mvt/)
[![Documentation Status](https://readthedocs.org/projects/mvt/badge/?version=latest)](https://docs.mvt.re/en/latest/?badge=latest)
[![CI](https://github.com/mvt-project/mvt/actions/workflows/python-package.yml/badge.svg)](https://github.com/mvt-project/mvt/actions/workflows/python-package.yml)
[![Downloads](https://pepy.tech/badge/mvt)](https://pepy.tech/project/mvt)

Mobile Verification Toolkit (MVT) is a collection of utilities to simplify and automate the process of gathering forensic traces helpful to identify a potential compromise of Android and iOS devices.

It has been developed and released by the [Amnesty International Security Lab](https://www.amnesty.org/en/tech/) in July 2021 in the context of the [Pegasus project](https://forbiddenstories.org/about-the-pegasus-project/) along with [a technical forensic methodology and forensic evidence](https://www.amnesty.org/en/latest/research/2021/07/forensic-methodology-report-how-to-catch-nso-groups-pegasus/).

*Warning*: MVT is a forensic research tool intended for technologists and investigators. Using it requires understanding the basics of forensic analysis and using command-line tools. This is not intended for end-user self-assessment. If you are concerned with the security of your device please seek expert assistance.


## Installation

MVT can be installed from sources or from [PyPi](https://pypi.org/project/mvt/) (you will need some dependencies, check the [documentation](https://docs.mvt.re/en/latest/install/)):

```
pip3 install mvt
```

For alternative installation options and known issues, please refer to the [documentation](https://docs.mvt.re/en/latest/install/) as well as [GitHub Issues](https://github.com/mvt-project/mvt/issues).


## Usage

MVT provides two commands `mvt-ios` and `mvt-android`. [Check out the documentation to learn how to use them!](https://docs.mvt.re/)


## License

The purpose of MVT is to facilitate the ***consensual forensic analysis*** of devices of those who might be targets of sophisticated mobile spyware attacks, especially members of civil society and marginalized communities. We do not want MVT to enable privacy violations of non-consenting individuals.  In order to achieve this, MVT is released under its own license. [Read more here.](https://docs.mvt.re/en/latest/license/)
