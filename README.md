<div align="center">
    <img src="logo.png" width="250">
</div>

# CGen
## About
CGen is a library that can easily and effortlessly generate your project structure.

## Installation
Prerequisites:
- Python 3.5 or higher

In order to install cgen - installation script is provided
```bash
curl https://raw.githubusercontent.com/Ph0enixKM/cgen/master/install.sh | bash
```

## Usage
CGen can be used easily from terminal
```bash
cgen
```
In order to target specific file use filename flag `--filename="path/to/file"`. CGen will look for configuration file. By default it's searches for `cgen.yaml` or `cgen.yml`.

**cgen.yml**
```yaml
libs:
  my-lib:
    - triangle
    - point
    - line
modules:
  - test
  - utils
settings:
  lang: c++
  # Default value is 'c'
  name: myProject
  # Defaults to 'Program'
  dir: path/to/project
  # Defaults to '.' which is cwd
```

## Uninstall
In order to uninstall cgen - removal script is provided
```bash
curl https://raw.githubusercontent.com/Ph0enixKM/cgen/master/uninstall.sh | bash
```
