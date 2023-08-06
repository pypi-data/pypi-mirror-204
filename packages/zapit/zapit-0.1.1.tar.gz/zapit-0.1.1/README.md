# Zapit

Zapit, a Zerotier API wrapper for Python.

## Installation

Zapit is supported on 3.8+. The recommended way to install Zapit is via pip.

``` bash
pip install zapit
```

## Quickstart

``` python

import zapit

ztcentral = zapit.Central(
    api_key = "API_KEY"
)

# Get all the networks avaliable.
networks = ztcentral.list_networks()
```
