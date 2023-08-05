# `astrodown`

[bold blue]Astrodown[/bold blue] is a toolkit to build interactive websites for data science projects.

See a live example at https://astrodown-playground.qiushiyan.dev :sparkles:

**Usage**:

```console
$ astrodown [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.


    Report [bold red]bugs[/bold red] on [link=https://github.com/astrodown/astrodown-web/]Github[/link]
    

**Commands**:

* `check`: Check for availabilities of programs...
* `dev`: [bold blue]Preivew[/bold blue] the website
* `docs`: [bold blue]Open[/bold blue] documentation...
* `init`: [bold blue]Create[/bold blue] an astrodown...
* `install`: [bold blue]Install[/bold blue] JavaScript...
* `new`: [bold blue]Create[/bold blue] the folder...
* `render`: [bold blue]Render[/bold blue] all Quarto...

## `astrodown check`

Check for availabilities of programs required by astrodown

**Usage**:

```console
$ astrodown check [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `astrodown dev`

[bold blue]Preivew[/bold blue] the website

**Usage**:

```console
$ astrodown dev [OPTIONS]
```

**Options**:

* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]
* `--port INTEGER`: port to run the website  [default: 3000]
* `--render-quarto / --no-render-quarto`: rerender quarto documents first  [default: no-render-quarto]
* `--help`: Show this message and exit.

## `astrodown docs`

[bold blue]Open[/bold blue] documentation websites for relevant tools, e.g. Quarto, Python, etc.

**Usage**:

```console
$ astrodown docs [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `astrodown init`

[bold blue]Create[/bold blue] an astrodown project.

Must have Quarto Node.js installed and avaiable in PATH variables, use `astrodown check` for health checks.

**Usage**:

```console
$ astrodown init [OPTIONS]
```

**Options**:

* `-p, --path TEXT`: path to create the project, default to the current working directory  [default: /Users/qiushi/workspace/astrodown/astrodown-python]
* `-n, --name TEXT`: name of the project
* `-pm, --package-manager [npm|yarn|pnpm]`: package manager to use, default to npm  [default: npm]
* `-t, --template [basic|full]`: template to use, default to basic  [default: basic]
* `--help`: Show this message and exit.

## `astrodown install`

[bold blue]Install[/bold blue] JavaScript dependencies.

Only need to be run once per project.

**Usage**:

```console
$ astrodown install [OPTIONS]
```

**Options**:

* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]
* `--help`: Show this message and exit.

## `astrodown new`

[bold blue]Create[/bold blue] the folder structure for a new analysis, dataset, model, api, etc.

**Usage**:

```console
$ astrodown new [OPTIONS] COMPONENT_TYPE:{analysis|dataset|model|shinyapp|api}
```

**Arguments**:

* `COMPONENT_TYPE:{analysis|dataset|model|shinyapp|api}`: the type of the component to be created  [required]

**Options**:

* `--help`: Show this message and exit.

## `astrodown render`

[bold blue]Render[/bold blue] all Quarto documents.

Should be run every time a Quarto document has changed. Edit _quarto.yml to include/exclude files.

**Usage**:

```console
$ astrodown render [OPTIONS]
```

**Options**:

* `--package-manager [npm|yarn|pnpm]`: package manager to use  [default: PackageManager.npm]
* `--help`: Show this message and exit.
