# nrp

This is a small package for computing roots of a given function using newton-raphson method.

The user needs to supply an initial root guess, the function as well as the first derivative of the function as callbacks.

## Usage

(We are actively adding supporting for passing functions as callback.)
**Example:**
```python
from nrp import newton_raphson
from lptypes import f64, i32


def check():
    x0: f64 = 20.0
    c: f64 = 3.0
    maxiter: i32 = 20
    x: f64
    x = newton_raphson(x0, c, maxiter)
    assert abs(x - 3.0) < 1e-5

check()
```
