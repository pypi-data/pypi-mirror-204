import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import click
import git
from git.exc import GitCommandError
from yaml import Loader, dump, load


def _colorize(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


def _read_yaml_file(file_path: str) -> str:
    with open(file_path) as f:
        content: str = f.read()
    return content


def _save_yaml_file(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        content: Any = dump(data, indent=4, default_flow_style=False)
        f.write(content)


def _get_target_tag(tags: list, all_versions: bool) -> str:
    if all_versions:
        return tags[0]
    for t in tags:
        if not any(v in t for v in ("a", "b", "rc")):
            return t
    return tags[0]


def _parse_tags(repo: dict) -> list:
    url: str = repo["repo"]
    try:
        remote_tags: list = (
            git.cmd.Git().ls_remote("--tags", url, sort="v:refname").split("\n")
        )
        tags: list = []
        for tag in remote_tags:
            parsed_tag: str = re.split(r"\t+", tag)[1]
            if parsed_tag.endswith("^{}"):
                continue
            parsed_tag = parsed_tag.replace("refs/tags/", "")
            tags.append(parsed_tag)
        return tags
    except GitCommandError:
        raise Exception(f"No tags found for repo: {url}")


def run(
    dry_run: bool, all_versions: bool, verbose: bool, exclude: tuple, keep: tuple
) -> None:
    os.environ["GIT_TERMINAL_PROMPT"] = "0"
    try:
        file_path: str = os.path.join(os.getcwd(), ".pre-commit-config.yaml")
        yaml_str: str = _read_yaml_file(file_path)
        data: Any = load(yaml_str, Loader)
        no_diff: list = []
        diff: list = []
        ignored: list = []
        kept: list = []

        with ThreadPoolExecutor(max_workers=10) as pool:
            tasks: list = []
            for i in range(len(data["repos"])):
                rep: dict = data["repos"][i]
                tasks.append(pool.submit(_parse_tags, rep))

        for i, repository in enumerate(data["repos"]):
            if not repository["repo"].startswith("http"):
                continue
            rep = data["repos"][i]
            repo_name: str = rep["repo"].split("/")[-1]
            tag_versions: list = tasks[i].result()
            tag_versions.reverse()
            target_ver: str = _get_target_tag(tag_versions, all_versions)
            if repo_name in exclude:
                ignored.append(
                    f"{repo_name} - {_colorize(rep['rev'] + ' ★', 'magenta')}"
                )
                continue
            if repo_name in keep:
                if rep["rev"] != target_ver:
                    kept.append(
                        f"{repo_name} - {_colorize(rep['rev'] + ' -> ' + target_ver + ' ◉', 'blue')}"
                    )
                else:
                    kept.append(f"{repo_name} - {_colorize(rep['rev'] + ' ◉', 'blue')}")
                continue
            if rep["rev"] != target_ver:
                diff.append(
                    f"{repo_name} - {_colorize(rep['rev'], 'yellow')} -> {_colorize(target_ver + ' ✘', 'red')}"
                )
                data["repos"][i]["rev"] = target_ver
            else:
                no_diff.append(f"{repo_name} - {_colorize(rep['rev'] + ' ✔', 'green')}")

        if verbose:
            click.echo("\n".join(ignored))
            click.echo("\n".join(kept))
            click.echo("\n".join(no_diff))

        if diff:
            click.echo("\n".join(diff))
            if not dry_run:
                _save_yaml_file(".pre-commit-config.yaml", data)
                click.echo(_colorize("Changes detected and applied", "green"))
            else:
                raise click.ClickException(_colorize("Changes detected", "red"))
        else:
            click.echo(_colorize("No changes detected", "green"))

    except Exception as ex:
        sys.exit(str(ex))


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry run only checks for the new versions without updating",
)
@click.option(
    "-a",
    "--all-versions",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include the alpha/beta versions when updating",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Display the complete output",
)
@click.option(
    "-e",
    "--exclude",
    multiple=True,
    default=[],
    help="Exclude specific repo(s) by the `repo` url trim",
)
@click.option(
    "-k",
    "--keep",
    multiple=True,
    default=[],
    help="Keep the version of specific repo(s) by the `repo` url trim (still checks for the new versions)",
)
def cli(dry_run: bool, all_versions: bool, verbose: bool, exclude: tuple, keep: tuple):
    run(dry_run, all_versions, verbose, exclude, keep)


if __name__ == "__main__":
    cli()
