![apartogether](https://github.com/trouchet/spycio/blob/master/images/spycio_tiny.png?raw=true)

[![Version](https://img.shields.io/pypi/v/spycio.svg)](https://pypi.python.org/pypi/spycio)
[![python](https://img.shields.io/pypi/pyversions/spycio.svg)](https://pypi.org/project/spycio/)
[![downloads](https://img.shields.io/pypi/dm/spycio)](https://pypi.org/project/spycio/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trouchet/spycio/HEAD)

[![codecov](https://codecov.io/gh/trouchet/spycio/branch/master/graph/badge.svg?token=65OGOH51NV)](https://codecov.io/gh/trouchet/spycio)
[![Lint workflow](https://github.com/trouchet/spycio/actions/workflows/check-lint.yaml/badge.svg)](https://github.com/trouchet/spycio/actions/workflows/check-lint.yaml)

Space with a (pseudo-)metric allows us to perform distances. This library offers several functionalities in this regard; 

How to install
================

We run the command on desired installation environment:

``` {.bash}
pip install spycio
```

Minimal example
================

``` {.bash}
#!/usr/bin/env python
from numpy import pi, Inf

from spycio import distance, travelTime
from spycio.utils import spherToGeo

def format_distance_without_configuration(A, B, speed, method):
    string_template='A:{origin}, B:{target}, speed:{speed}, method:{on}, distance:{d}, eta:{eta}'
    
    dist=distance(A, B, method)
    duration=travelTime(speed, A, B, method)
    
    return string_template.format(origin=A,target=B,speed=speed, on=method,d=dist,eta=duration)

def format_distance(A, B, speed, method, config):
    string_template='A:{origin}, B:{target}, speed:{speed}, method:{on}, config:{setup}, distance:{d}, eta:{eta}'
    
    dist=distance(A, B, method, config)
    duration=travelTime(speed, A, B, method, config)
    
    return string_template.format(origin=A,target=B, speed=speed, on=method,setup=config, d=dist, eta=duration)


# Default distance calculation: Euclidean
A=[0, 0]
B=[1, 1]
C=[2, 2]
D=[pi / 2, 0]

speed=1

print('Euclidean distance: '+str(distance(A, B)))

print('\n')

configurations=[
    (B, C, speed, "manhattan"),
    (B, C, speed, "euclidean"),
    (B, C, speed, "max"),
    (B, C, speed, "chebyshev"),
    (B, C, speed, "manhattan"),
    (B, C, speed, "cityblock"),
    (B, C, speed, "cosine"),
    (B, C, speed, "braycurtis"),
    (B, C, speed, "canberra")
]

print('Format distance without configuration: ')
for origin, target, speed, method in configurations:
    print(format_distance_without_configuration(origin, target, speed, method))

print('\n')

configurations=[
    (B, C, speed, "pnorm", { "exponent": 2 }),
    (B, C, speed, "pnorm", { "exponent": 3 }),
    (B, C, speed, "pnorm", { "exponent": 4 }),
    (B, C, speed, "pnorm", { "exponent": Inf }),
    (A, D, speed, "sphere", { "radius": 1 }),
    (spherToGeo(A), spherToGeo(D), speed, "geographical", { "radius": 1 })
]

print('Format distance with configuration: ')

for origin, target, speed, method, config in configurations:
    print(format_distance(origin, target, speed, method, config))
```