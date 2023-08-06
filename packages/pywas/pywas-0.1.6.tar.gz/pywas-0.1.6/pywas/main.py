import os
from rich import print
import typer
from .wrapper.ngspice import ng_spice
from .wrapper.base_wrapper import write_conf
from pywas.template import template
from cookiecutter.main import cookiecutter


help_str = """
*Py*thon *W*rapper for *A*nalog design *S*oftware

**Installation using [pipx](https://pypa.github.io/pipx/installation/)**:

```console
$ pipx install pywas
```
"""
cli = typer.Typer(help=help_str)
cli.add_typer(ng_spice, name="ngspice", help="ngspice utility")
cli.add_typer(template, name="template", help="templating part")


@cli.command("create")
def new_project(name: str):
    """
    Create a new project with specified options.
    """
    template_path = "./pywas/cookiecutter_template"
    cookiecutter(os.path.join(template_path, name))


if __name__ == "__main__":
    cli()
