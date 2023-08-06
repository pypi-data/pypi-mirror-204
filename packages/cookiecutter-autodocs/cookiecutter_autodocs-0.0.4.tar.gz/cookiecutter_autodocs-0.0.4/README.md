# cookiecutter-autodocs

Generate docs for a cookiecutter template's inputs. Pre-commit hook and github-action

## Why?

[Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) is a powerful tool to create templates for all sorts of projects, but
one of its downsides is it relies on a plain JSON file for its input (cookiecutter.json). Because JSON does not allow comments, you cannot
document your inputs without writing the documentation separately.

cookiecutter-autodocs allows you to write your Cookiecutter's input as a Toml file, cookiecutter.desc. In this file you can add defaults, info about the variable type,
and a description of each variable.

An example cookiecutter.desc

```toml
[project_slug]
default = "new_project"
description = "The name of the project."
type = "string"

[python_version]
default = "3.11.2"
description = "What python version to use with this project"
type = "string"

[dev_requirements]
default = []
description = "What dev requirements does this project have"
type = "list(string)"

[author]
default = ""
description = "Who's the author?"
type = "string"
```

You can then generate a `cookiecutter.json` from this `cookiecutter.desc` file.

```shell
cookiecutter-autodocs generate cookiecutter -i cookiecutter.decs -o cookiecutter.json
cat cookiecutter.json
{
    "project_slug": "new_project",
    "python_version": "3.11.2",
    "dev_requirements": [],
    "author": ""
}
```

You can also use the `cookiecutter.desc` file to generate additional documentation, like a markdown table:

```shell
cookiecutter-autodocs generate markdown -i cookiecutter.desc
```

```
+-----------------------------------------------------------------------------------------------+
|      name      |                 description                |  default  |    type    |required|
+----------------+--------------------------------------------+-----------+------------+--------+
|  project_slug  |          The name of the project.          |new_project|   string   |  False |
+----------------+--------------------------------------------+-----------+------------+--------+
| python_version |What python version to use with this project|   3.11.2  |   string   |  False |
+----------------+--------------------------------------------+-----------+------------+--------+
|dev_requirements|What dev requirements does this project have|     []    |list(string)|  False |
+----------------+--------------------------------------------+-----------+------------+--------+
|     author     |              Who's the author?             |           |   string   |  True  |
+-----------------------------------------------------------------------------------------------+
```

## Installation

### CLI

```shell
pip install cookiecutter-autodocs
```

## Documentation

See [ReadTheDocs](https://cookiecutter-autodocs.readthedocs.io/en/latest/) for usage and more detailed documentation.
