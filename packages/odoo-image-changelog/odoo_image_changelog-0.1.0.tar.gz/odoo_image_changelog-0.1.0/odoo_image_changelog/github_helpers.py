from datetime import datetime
from datetime import timedelta

from github import Github
from github.GithubObject import NotSet
from github.GithubException import UnknownObjectException


class GithubHelper(object):
    def __init__(self, token: str, repository: str) -> None:
        self.token = token
        self.repository = repository
        self.github_instance = self._get_instance()
        self.repo_instance = self._get_repo()

    def _get_instance(self) -> Github:
        if not self.token:
            return Github()
        else:
            return Github(self.token)

    def _get_repo(self):
        if "/" not in self.repository:
            self.repository = f"camptocamp/{self.repository}"

        return self.github_instance.get_repo(self.repository)

    def get_content(self, path: str = "", ref: str = NotSet):
        return self.repo_instance.get_contents(path, ref=ref)

    def get_hash(self, branch: str):
        branch_repo = self.repo_instance.get_branch(branch)
        return branch_repo.commit.sha

    def get_changelog(self, branch: str, previous_hash: str, current_hash: str):
        if not current_hash:
            # current hash is not present like in unstable we take head
            to_hash = self.get_hash(branch)
        else:
            to_hash = current_hash
        current_repo = self.repo_instance
        branch_repo = current_repo.get_branch(branch)
        commit_list = []
        if not previous_hash:
            return ["feat : First Release"], to_hash
        else:
            since_date = current_repo.get_commit(
                previous_hash
            ).commit.author.date + timedelta(seconds=1)
            to_date = current_repo.get_commit(to_hash).commit.author.date + timedelta(
                seconds=1
            )
            commits_list = current_repo.get_commits(
                sha=branch, since=since_date, until=to_date
            )
            for commit_info in commits_list:
                if commit_info.commit.message.startswith("[I18N]"):
                    continue
                commit_string = commit_info.commit.message.split("\n")[0]
                commit_struct = f"{commit_string}, ({commit_info.commit.url}) \n\n"
                commit_list.append(commit_struct)

        return commit_list, branch_repo.commit.commit.sha

    def get_commit_date(self, commit_sha: str):
        commit_date = self.repo_instance.get_commit(commit_sha).commit.author.date
        return commit_date

    def has_modifications(self, path: str, since: datetime):
        commits = self.repo_instance.get_commits(path=path, since=since)
        return bool(commits.totalCount)

    def create_branch(self, branch_name: str, base_branch: str):
        branch = self.repo_instance.get_branch(base_branch)
        self.repo_instance.create_git_ref(
            f"refs/heads/{branch_name}", branch.commit.sha
        )
        return self.repo_instance.get_branch(branch_name)

    def delete_branch(self, branch_name):
        try:
            ref = self.repo_instance.get_git_ref(f"heads/{branch_name}")
            ref.delete()
        except UnknownObjectException:
            print("No such branch", branch_name)

    def update_file(
        self,
        branch_name: str,
        path: str,
        message: str,
        content: str,
        sha: str,
    ):
        self.repo_instance.update_file(path, message, content, sha, branch_name)

    def update_changelog(
        self,
        running_version: str,
        changelog_file: str,
        changelog_content: str,
        hash_file_content: str,
        hash_file_path: str,
        base_branch: str,
        new_branch_name: str,
    ):
        current_file_hash = self.get_content(changelog_file, base_branch)
        self.update_file(
            new_branch_name,
            changelog_file,
            f"feat: Changelog Change {running_version}",
            changelog_content,
            current_file_hash.sha,
        )
        old_file_hash = self.get_content(hash_file_path, base_branch)
        self.update_file(
            new_branch_name,
            hash_file_path,
            f"feat: hash Change {running_version}",
            hash_file_content,
            old_file_hash.sha,
        )

    def create_pull_request(
        self,
        commit_message: str,
        branch: str,
        base_branch: str,
    ):
        # If multiline,
        # assuming format with title in first line, one empty line, then body
        if "\n" in commit_message:
            title, _, *body = commit_message.split("\n")
            body = "\n".join(body)
        else:
            title = commit_message
            body = ""

        new_pr = self.repo_instance.create_pull(
            title=title,
            body=body,
            base=base_branch,
            head=branch,
        )
        new_pr.set_labels("robot")
        return new_pr
