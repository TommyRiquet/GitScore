''' GitScore class to score a git repository '''
import re
import requests


class GitScore:
    ''' Class to score a git repository '''

    def __init__(self):
        self.git_score = 0
        self.commit_count = 0
        self.duplicate_commits = []
        self.merge_commits = []
        self.conventional_commits = False

    def get_score(self, url):
        ''' Gets the git score for the repository '''

        repo_informations = self.get_repo_informations(url)

        if repo_informations is None or 'message' in repo_informations:
            return None

        all_commits = self.get_all_commits(
            repo_informations['owner']['login'], repo_informations['name'])

        if all_commits is None or len(all_commits) == 0:
            return None

        commit_count = self.get_commit_count(all_commits)

        duplicate_commits = self.get_duplicate_commits(all_commits)
        merge_commits = self.get_merge_commits(all_commits)

        git_score = self.get_git_score(
            commit_count, duplicate_commits, merge_commits)

        is_conventional_commits = self.is_repo_following_conventionnal_commits(
            all_commits)

        return {
            'repo_name': repo_informations['name'],
            'repo_description': repo_informations['description'],
            'repo_language': repo_informations['language'],
            'owner_name': repo_informations['owner']['login'],
            'total_commits': commit_count,
            'duplicate_commits': duplicate_commits,
            'merge_commits': merge_commits,
            'conventional_commits': is_conventional_commits,
            'git_score': git_score
        }

    def get_repo_informations(self, url):
        ''' Gets the repository informations
            :param url: The url to the git repository
        '''
        try:
            repo_owner = url.split('/')[0]
            repo_name = url.split('/')[1]

            response = requests.get(
                f'https://api.github.com/repos/{repo_owner}/{repo_name}',
                timeout=5
            )
            return response.json()

        except (TypeError, IndexError):
            return None

    def get_all_commits(self, repo_owner, repo_name):
        ''' Gets the git commits for the repository
            :param url: The url to the git repository
        '''
        try:
            all_commits = []

            def fetch_commits(page):
                response = requests.get(
                    f'https://api.github.com/repos/{repo_owner}/{repo_name}' +
                    f'/commits?per_page=100&page={page}',
                    timeout=5
                )
                return response.json()

            page = 1
            response_data = fetch_commits(page)

            while response_data:
                all_commits.extend([commit['commit']['message']
                                    for commit in response_data])
                page += 1
                response_data = fetch_commits(page)

        except (TypeError, IndexError):
            all_commits = None

        return all_commits

    def get_commit_count(self, all_commits):
        ''' Gets the total number of commits
            :param all_commits: The git log
        '''
        return len(all_commits)

    def get_git_score(self, commit_count, duplicate_commits, merge_commits):
        ''' Gets the git score for the repository
            :param commit_count: The total number of commits
            :param duplicate_commits: The duplicate commits
            :param merge_commits: The merge commits
        '''
        git_score = 0
        if commit_count > 0:
            git_score = 100 - (len(duplicate_commits) +
                               len(merge_commits)) / commit_count * 100
        return self.get_letter_grade(git_score)

    def get_letter_grade(self, git_score):
        ''' Gets the letter grade for the git score
            :param git_score: The git score
        '''
        grade_ranges = [(98, "A+"), (93, "A"), (90, "A-"), (87, "B+"), (83, "B"), (80, "B-"),
                        (77, "C+"), (73, "C"), (70, "C-"), (67, "D+"), (63, "D"), (60, "D-")]
        for score, grade in grade_ranges:
            if git_score >= score:
                return grade

        return "F"

    def get_duplicate_commits(self, all_commits):
        ''' Checks for duplicate commits in the git log
            :param all_commits: The git log 
        '''
        duplicate_commits = []

        for commit in all_commits:
            if all_commits.count(commit) > 1:
                duplicate_commits.append(commit)
        return duplicate_commits

    def get_merge_commits(self, all_commits):
        ''' Checks for merge commits in the git log
            :param all_commits: The git log
        '''
        merge_commits = []

        for commit in all_commits:
            if "Merge" in commit:
                merge_commits.append(commit)
        return merge_commits

    def is_repo_following_conventionnal_commits(self, all_commits):
        ''' Checks if the repository is following the conventional commits
                :param all_commits: The git log 
        '''
        for commit in all_commits[:-1]:
            if re.match(
                r'^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)' +
                    r'{1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)', commit):
                continue
            else:
                return False
        return True
