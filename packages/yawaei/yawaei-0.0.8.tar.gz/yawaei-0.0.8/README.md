# Yet Another Wrapper Around Epitech Intranet
This project still contains Work in progress.

The goal of the project is to centralize to a single library, data exchange methods around the Epitech intranet.

The final form of this project will be a package that can be imported inside python scripts and projects.

# Installation

```sh
pip install Yawaei
```

# Usage

```python
import Yawaei

token = "<intranet-autologin-token>"

Intra = Yawaei.intranet.AutologinIntranet(token)
```

# Content
## [`abc.py`](src/Yawaei/abc.py)
`Intranet` interface
## [`intranet.py`](src/Yawaei/intranet.py)
`AutologinIntranet` implementation of `Intranet` interface

# For developpers
A [`Makefile`](./Makefile) is available inside the repository to build and upload to pypi for test and prod.