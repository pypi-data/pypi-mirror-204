import os
import sys
import random
import string
from ruamel.yaml.main import YAML
from .github_helpers import GithubHelper


ODOO_REPO = os.environ.get("ODOO_REPO", "odoo/odoo")
DOCKER_ODOO_REPO = os.environ.get("DOCKER_ODOO_REPO", "camptocamp/docker-odoo-core")
BASE_BRANCH = os.environ.get("BASE_BRANCH", "build_testing")


def get_previous_unstable_rev(current_running_build):
    yaml = YAML()
    values_yaml = False
    with open(f"local_repo/{current_running_build}/HASH_UNSTABLE") as yaml_file:
        values_yaml = yaml.load(yaml_file.read())
    # We clean current_hash to take the head ref
    values_yaml["current_hash"] = ""
    return values_yaml


def get_previous_stable_rev(current_running_build):
    yaml = YAML()
    values_yaml = False
    with open(f"local_repo/{current_running_build}/HASH_STABLE") as yaml_file:
        values_yaml = yaml.load(yaml_file.read())
    return values_yaml


def hash_to_string(data):
    string_data = ""
    if "previous_hash" in data:
        previous_commit = data["previous_hash"]
        string_data += f"previous_hash: {previous_commit}\n"
    if "current_hash" in data:
        current_commit = data["current_hash"]
        string_data += f"current_hash: {current_commit}\n"
    return string_data


def generate_changelog(
    githubinstance, current_running_build: str, new_branch_name: str, stable: bool
):
    if stable:
        hash_yaml = get_previous_stable_rev(current_running_build)
        hash_file = f"{current_running_build}/HASH_STABLE"
    else:
        hash_yaml = get_previous_unstable_rev(current_running_build)
        hash_file = f"{current_running_build}/HASH_UNSTABLE"
        # We reset the current_hash for stable
        hash_yaml["current_hash"] = ""

    content_array = []
    githubodooinstance = GithubHelper(githubinstance.token, ODOO_REPO)
    changelog_array, current_hash = githubodooinstance.get_changelog(
        current_running_build,
        hash_yaml["previous_hash"],
        hash_yaml["current_hash"],
    )
    if changelog_array:
        if stable:
            change_log_file = f"{current_running_build}/CHANGELOG.md"
        else:
            change_log_file = f"{current_running_build}/CHANGELOG_UNSTABLE.md"

        with open(f"local_repo/{change_log_file}") as file:
            while line := file.readline().rstrip():
                content_array.append(line)
        previous_hash = hash_yaml["previous_hash"]
        title_change_log = f"\nChangelog: from {previous_hash} to {current_hash}\n"
        line = len(title_change_log) * "-"
        content_array.append(title_change_log)
        content_array.append("\n")
        content_array.append(line)
        content_array.append("\n\n")
        content_array = content_array + changelog_array
        changelog_string = "".join(content_array)
        # Update version tags
        # if not stable we can update hash autmatically
        # for stable do it manually and tag release as stable
        if not stable:
            # if no previous hash we just set previous_hash as the
            # current one
            if not previous_hash:
                hash_yaml["previous_hash"] = current_hash
            else:
                hash_yaml["previous_hash"] = previous_hash
            hash_yaml["current_hash"] = current_hash
        # Then we will update it
        githubinstance.update_changelog(
            current_running_build,
            change_log_file,
            changelog_string,
            hash_to_string(data=hash_yaml),
            hash_file,
            BASE_BRANCH,
            new_branch_name,
        )
        return True
    else:
        return False


def main(args=None):
    github_token = os.environ.get("ROBOT_TOKEN", False)
    build_list = os.environ.get("BUILD_CHANGELOG_LIST", False)
    build_array = build_list.split(",")
    github_tag = os.environ.get("GITHUB_REF", False)
    # Create branch for this commit
    new_branch_name = f"{BASE_BRANCH}-{''.join(random.choice(string.ascii_uppercase) for _ in range(7))}"
    gitinstance = GithubHelper(github_token, DOCKER_ODOO_REPO)
    gitinstance.create_branch(new_branch_name, BASE_BRANCH)
    had_changes = False
    for build_instance in build_array:
        if "stable" in github_tag:
            changes_detected = generate_changelog(
                gitinstance, build_instance, new_branch_name, stable=True
            )
        else:
            changes_detected = generate_changelog(
                gitinstance, build_instance, new_branch_name, stable=False
            )
        if changes_detected and not had_changes:
            had_changes = True
    if had_changes:
        gitinstance.create_pull_request(
            "feat: Automatic Changelog update",
            new_branch_name,
            BASE_BRANCH,
        )
    else:
        gitinstance.delete_branch(new_branch_name)


if __name__ == "__main__":
    main(sys.argv[1:])
