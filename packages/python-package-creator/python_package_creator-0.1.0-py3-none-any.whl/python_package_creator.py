import click
import requests
import os
import subprocess
import toml
from appdirs import user_config_dir
from pathlib import Path
from cookiecutter.main import cookiecutter

CONFIG_FILE_NAME = "my_cli.toml"
DEFAULT_COOKIECUTTER_URL = "https://github.com/chrisdexler/cookiecutter-pypackage"


def check_name_availability(name):
    response = requests.get(f"https://pypi.org/pypi/{name}/json")
    if response.status_code == 200:
        return False
    return True


def create_github_repository(name, organization=None, token=None):
    url = "https://api.github.com/user/repos" if not organization else f"https://api.github.com/orgs/{organization}/repos"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return response.json()["ssh_url"]
    else:
        return None


def read_config():
    config_path = Path(user_config_dir()) / CONFIG_FILE_NAME
    if not config_path.exists():
        config = {"cookiecutter_url": DEFAULT_COOKIECUTTER_URL}
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            toml.dump(config, f)
    else:
        with open(config_path, "r") as f:
            config = toml.load(f)
    return config


@click.command()
@click.argument("name")
@click.option("-o", "--org", help="Organization for creating the repository")
def create_project(name, org):
    if not check_name_availability(name):
        raise click.ClickException(f"Error: Package name {name} is not available on PyPI")

    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        raise click.ClickException("Error: GITHUB_TOKEN environment variable is not set")

    repo_url = create_github_repository(name, organization=org, token=token)
    if repo_url is None:
        raise click.ClickException(f"Error: Unable to create a new repository with the name {name}")

    config = read_config()
    cookiecutter_url = config["cookiecutter_url"]
    cookiecutter(cookiecutter_url, extra_context={"repo_name": name})

    subprocess.run(["git", "init"], cwd=name)
    subprocess.run(["git", "add", "-A"], cwd=name)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=name)
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=name)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=name)

    click.echo(f"Project {name} created and pushed to {repo_url}")


if __name__ == "__main__":
    create_project()
