# webviz-dev-sync

`webviz-dev-sync` is a developer tool that helps syncing different online and offline versions of the four major Webviz packages:
- `webviz-config`
- `webviz-subsurface`
- `webviz-core-components`
- `webviz-subsurface-components`

`webviz-dev-sync` can be used both as a CLI and a GUI app. The packages are managed in a YAML config file.

# Installation

> **__IMPORTANT:__**  Please make sure to install `webviz-dev-sync` in the same virtual environment you are using for the other Webviz packages.

## Using pypi

`pip install webviz-dev-sync`

## Using Git

```bash
git clone https://github.com/equinor/webviz-dev-sync.git
cd ./webviz-dev-sync
pip install -e .
```
> **__NOTE:__**  The GUI requires `tkinter` to be installed. If you don't have it installed yet, please follow the steps below.


## Installing `tkinter` in a virtual environment

Unfortunately, `tkinter` cannot be added to an already existing virtual environment. In order to install it anyways, follow the steps below.
1) Activate your virtual environment
```bash
source <path to virtualenv>/bin/activate
```
2) Freeze your installed packages
```bash
pip freeze > requirements.txt
```
3) Deactivate your virtual environment
```bash
deactivate
```
4) Install `python-tk`
```bash
sudo apt-get install python3-tk
```
5) Recreate your virtual environment
```bash
virtualenv <name of your environment> --system-site-packages
# Note:
# You might need to install virtualenv first
# pip install virtualenv
```
6) Activate your virtual environment
```bash
source <path to virtualenv>/bin/activate
```
7) Restore all formerly installed packages
```bash
pip install -r requirements.txt
```

# Usage
After installation `webviz-dev-sync` can be accessed via 
```bash
webviz-dev $args
```

Two different arguments are supported:

## `webviz-dev start`

This command starts the syncing process. It potentially downloads all required packages from Github, installs and builds code and performs the linking actions if requested.

Optionals Arguments:

`--gui`: Opens the GUI as a tray icon application. Requires `tkinter` to be installed (see above). A right-click on the icon opens a menu with multiple actions.

> **__NOTE:__**  When starting the application for the first, you will be asked for a Github access token in the console/terminal you called the command from. See below for more information.

## `webviz-dev config`

This command opens the config file in your preferred text editor (see below for config options).

# Configuration

The configuration is set in the applications `config.yaml` file which is stored in the user's data directory. The config file can easily be accessed by
calling the `webviz-dev config` command. The config consists of three global settings and a set of settings for each single package.

## Global settings

### `editor`:
By changing this option you can define which editor is used for opening the config file when calling `webviz-dev config`. Defaults to your system's default editor.

### `github-access-token`:
An access token for Github. This is required in order to get access to all Webviz repositories and branches on Github. The application will automatically ask 
you for this token when starting it for the first time. See here for instructions to create a token for your Github account: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token.

### `repo-storage-directory`
You can use this option to set in which directory the Github packages shall be cloned to when non-local packages are used. This defaults to the application's folder in your user directory.

### `packages`
This object contains all four major Webviz packages and their individual settings.

## Package-specific settings

Each package can be individually configured. You can either use an already installed/cloned local package (e.g. if you want to control the package's state manually) or let `webviz-dev-sync` automatically handle it for you.

### Use a local package

If you want to use a local package, set the `local_path` option to your local package directory.

```yaml
<package-name>:
  local_path: <path to your local package>
```

### Use a Github branch

If you want to use the current head commit of a Github branch, set the `github_branch` option.

```yaml
<package-name>:
  github_branch:
    branch: <name of the branch, e.g. master>
    repository: <name of the Github repository, e.g. equinor/webviz-config>
```

### Optional settings

The package `webviz-subsurface-components` will be automatically linked to your local package of `webviz-core-components`. This makes it easier to debug/evaluate changes that were made to components in `webviz-core-components` in other packages like `webviz-subsurface` and you don't have to take care of linking yourself. However, if you prefer to use the version of `webviz-core-components` that is provided by `npm` (you will not be able to test branches of `webviz-core-components` in other packages), you can set the option `link_package` to `false`. This option defaults to `true`.

```yaml
webviz-subsurface-components:
  link_package: false
  ...
```
