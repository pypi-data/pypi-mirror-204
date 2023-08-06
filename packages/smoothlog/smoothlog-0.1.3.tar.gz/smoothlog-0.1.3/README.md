## smoothlog

A modern, easy to use logger written in Python.

## Key Features

- Simple and readable output.
- Colored terminal for easier debugging.
- File management system for easy retracing.
- No external libraries required.

## Installing

**Python 3.8 or higher is required**

To install the library you should run the following command:

```shell
# Linux/macOS
python3 -m pip install -U smoothlog

# Windows
py -3 -m pip install -U smoothlog
```
> Note: This package isn't registered yet

## Quick Example

```python
import smoothlog

log = smoothlog.getLogger("logger")

log.info("Hello World!")
log.warn("Uh oh World!")
log.fail("Bye-bye World!")
```
Console Output:

![](https://i.imgur.com/FGg1quK.png)

You can find examples in the examples directory.
