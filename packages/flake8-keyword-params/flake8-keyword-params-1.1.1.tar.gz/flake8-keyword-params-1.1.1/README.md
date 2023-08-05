# [flake8-keyword-params](https://github.com/plinss/flake8-keyword-params)

flake8 plugin to require that optional parameters are keyword-only.

This is a highly opinionated plugin asserting that optional parameters should be keyword-only (see PEP-3102).
Requiring keywords for optional parameters generally improves readability at point of use,
especially for parameters that are seldomly used 
or would otherwise fall into the [bool trap](https://adamj.eu/tech/2021/07/10/python-type-hints-how-to-avoid-the-boolean-trap/).

Accepting that there are common use cases where a keyword parameter offers little value,
this plugin allows a safelist of function names and parameters that are allowed to be optional.
A small predefined set is included by default,
but may be extended or replaced via config options.
Feel free to file issues to request more default safe entries,
especially any in the Python standard library.  

## Installation

Standard python package installation:

    pip install flake8-keyword-params


## Options

`keyword-params-safelist`
: Add a function to the safelist, may be specified more than once 

`keyword-params-exclude-safelist`
: Remove a function from the safelist, may be specified more than once 

`keyword-params-include-name`
: Include plugin name in messages

`keyword-params-no-include-name`
: Do not include plugin name in messages (default setting)

All options may be specified on the command line with a `--` prefix,
or can be placed in your flake8 config file.

Safelist options may specify a bare function name, 
so that all parameters are allowed to be optional without keywords, 
or a function name, followed by a colon, followed by a parameter name.
In the latter case, only the specified parameters may be optional without keywords.
Both function names and parameter names may be regular expressions.

For example:
```
flake8 --keyword-params-safelist=get:default --keyword-params-safelist="from_.*:default"
```
in .flake8 or setup.cfg
```
[flake8]
keyword-params-safelist = get:default from_.*:default
```
or in pyproject.toml:
```
[tool.flake8]
keyword-params-safelist = ['get:default', 'from_.*:default']
```


## Error Codes

| Code   | Message |
|--------|---------|
| KWP001 | Optional parameter 'param' should be keyword only


## Examples

```
def foo(x=None):  <-- KWP001

def get(key, default=None):  <-- No error, common use case
```