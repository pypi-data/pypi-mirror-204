# `pyWAS`

*Py*thon *W*rapper for *A*nalog design *S*oftware

**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:

```console
$ pipx install pywas
```

**Usage**:

```console
$ pyWAS [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new project with specified options.
* `ngspice`: ngspice utility
* `template`: templating part

## `pyWAS create`

Create a new project with specified options.

**Usage**:

```console
$ pyWAS create [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

## `pyWAS ngspice`

ngspice utility

**Usage**:

```console
$ pyWAS ngspice [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `config`
* `install`: Install ngspice executable in the correct...
* `run`: Should not be named "run"

### `pyWAS ngspice config`

**Usage**:

```console
$ pyWAS ngspice config [OPTIONS] KEY PATH
```

**Arguments**:

* `KEY`: [required]
* `PATH`: [required]

**Options**:

* `--help`: Show this message and exit.

### `pyWAS ngspice install`

Install ngspice executable in the correct location.

**Usage**:

```console
$ pyWAS ngspice install [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `pyWAS ngspice run`

Should not be named "run"

**Usage**:

```console
$ pyWAS ngspice run [OPTIONS] IN_FILE
```

**Arguments**:

* `IN_FILE`: [required]

**Options**:

* `--out-folder TEXT`: [default: C:\Users\JoPo\PycharmProjects\pyWES/tmp/]
* `--help`: Show this message and exit.

## `pyWAS template`

templating part

**Usage**:

```console
$ pyWAS template [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new file from the given template.
* `infos`: Give a description of the template.
* `list`: List all available template.

### `pyWAS template create`

Create a new file from the given template.
List of available template can be retrieve by ```pywas template list```

**Usage**:

```console
$ pyWAS template create [OPTIONS] TEMPLATE_NAME
```

**Arguments**:

* `TEMPLATE_NAME`: [required]

**Options**:

* `--output-file PATH`
* `--help`: Show this message and exit.

### `pyWAS template infos`

Give a description of the template.

**Usage**:

```console
$ pyWAS template infos [OPTIONS] TEMPLATE_NAME
```

**Arguments**:

* `TEMPLATE_NAME`: [required]

**Options**:

* `--help`: Show this message and exit.

### `pyWAS template list`

List all available template.

**Usage**:

```console
$ pyWAS template list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
