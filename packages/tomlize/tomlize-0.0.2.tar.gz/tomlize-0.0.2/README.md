# tomlize

Move the configuration of all your tools to `pyproject.toml`.

```
$ python -m tomlize --help
usage: __main__.py [-h] input_file [output_file]

positional arguments:
  input_file
  output_file

options:
  -h, --help   show this help message and exit

```

The tool can be used to port the configuration from the following files:

## `setup.py`

```
python -m tomlize setup.py pyproject.toml
```