import os
import subprocess
from typing import Optional
import typer
from typer import Typer
from pathlib import Path
from astrodown.templates import get_template_path
from astrodown.cli.check import (
    print_health_table,
    command_path,
    required_programs,
)
from astrodown.cli.init import create_project, Template
from astrodown.cli.utils import (
    colored_text,
    get_package_manager,
    prompt_success,
    run_shell,
)
from astrodown.cli.install import PackageManager
from rich import print
from astrodown.cli.new import ComponentType, new_component

__version__ = "0.1.16"


app = Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    epilog="""
    Report [bold red]bugs[/bold red] on [link=https://github.com/astrodown/astrodown-web/]Github[/link]
    """,
)


@app.command()
def init(
    path: Optional[Path] = typer.Option(
        os.getcwd(),
        "--path",
        "-p",
        prompt="Project Directory",
        help="path to create the project, default to the current working directory",
        writable=True,
    ),
    name: str = typer.Option(
        "hello-astrodown",
        "--name",
        "-n",
        help="name of the project",
        show_default=False,
        prompt="Project Name",
    ),
    package_manager: PackageManager = typer.Option(
        "npm",
        "--package-manager",
        "-pm",
        prompt="Node.js Package Manager",
        help="package manager to use, default to npm",
    ),
    template: Template = typer.Option(
        "full",
        "--template",
        "-t",
        prompt="Template",
        help="template to use, default to basic",
    ),
):
    """
    [bold blue]Create[/bold blue] an astrodown project.

    Must have Quarto Node.js installed and avaiable in PATH variables, use `astrodown check` for health checks.
    """
    path = path.expanduser().resolve()
    all_required_programs = [*required_programs, package_manager]
    program_availabilities = {
        program: command_path(program) for program in all_required_programs
    }

    for program in program_availabilities:
        if program_availabilities[program] is None:
            print(
                colored_text(
                    "Some of the required programs are not installed, see the table below for details",
                    color="red",
                )
            )
            print_health_table(program_availabilities)
            raise typer.Exit()

    prompt_success(
        f"creating project {colored_text(name)} at {colored_text(path)} with package manager {package_manager}"
    )

    template_path = get_template_path(template)
    result_path = create_project(
        template_path,
        output_dir=path,
        extra_context={
            "project_name": name,
            "project_title": name.replace("-", " ").title(),
            "package_manager": package_manager.value,
        },
    )

    prompt_success(
        "project creation successful, run the following commands to get started"
    )
    print(
        f"""
    cd {result_path}
    astrodown install
    astrodown dev --render-quarto
    """
    )


@app.command()
def render():
    """
    [bold blue]Render[/bold blue] all Quarto documents.

    Should be run every time a Quarto document has changed. Edit _quarto.yml to include/exclude files.
    """
    return run_shell("quarto render")


@app.command()
def install(
    package_manager: PackageManager = typer.Option(
        get_package_manager(verbose=False), help="package manager to use"
    ),
):
    """
    [bold blue]Install[/bold blue] JavaScript dependencies.

    Only need to be run once per project.
    """
    return run_shell(f"{package_manager} install")


@app.command()
def dev(
    package_manager: PackageManager = typer.Option(
        get_package_manager(verbose=False), help="package manager to use"
    ),
    port: Optional[int] = typer.Option(3000, help="port to run the website"),
    render_quarto: Optional[bool] = typer.Option(
        False, help="render quarto documents first before starting the website"
    ),
    reload: Optional[bool] = typer.Option(
        True,
        help="reload the website when files change (use `quarto preview` in a separate process)",
    ),
):
    """
    [bold blue]Preivew[/bold blue] the website

    if --render-quarto is set, all quarto documents will be rendered before the website is started. Set this if it's the first time you're running the website or you've made changes to the quarto documents.

    if --reload is set, the website preview will be updated when quarto documents change. This is achieved by calling `quarto preview` in a separate process
    """
    if render_quarto:
        prompt_success("rendering quarto documents")
        run_shell("quarto render")
    if reload:
        run_shell("quarto preview --no-serve", verbose=False, background=True)
    prompt_success("previewing the website")
    run_shell(f"{package_manager} run dev --port {port}")


@app.command(rich_help_panel="Utils")
def new(
    component_type: ComponentType = typer.Argument(
        ..., help="the type of the component to be created"
    ),
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name",
        help="Name for analysis/data/model/shinyapp",
    ),
):
    """
    [bold blue]Create[/bold blue] the folder structure for a new analysis, dataset, model, api, etc.
    """
    return new_component(component_type, name)


@app.command(rich_help_panel="Utils")
def docs():
    """
    [bold blue]Open[/bold blue] documentation websites for relevant tools, e.g. Quarto, Python, etc.

    TBD
    """
    pass


@app.command(rich_help_panel="Utils")
def check():
    """
    Check for availabilities of programs required by astrodown
    """
    missing_programs = print_health_table()
    if len(missing_programs) == 0:
        print("All things installed," + colored_text(" you are good to go!"))
    else:
        print(
            "The following tools are missing "
            f"{colored_text(missing_programs, color='red')}\n"
            "please make sure they are installed and available in PATH variables"
        )


def version_callback(value: bool):
    if value:
        print(f"Astrodown: {__version__}")
        raise typer.Exit()


@app.callback(context_settings={"ignore_unknown_options": True})
def callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    """
    [bold blue]Astrodown[/bold blue] is a toolkit to build interactive websites for data science projects.

    See a live example at https://astrodown-playground.qiushiyan.dev :sparkles:
    """


if __name__ == "__main__":
    app()
