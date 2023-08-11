''' GitScore class to score a git repository '''
import os
import re


class GitScore:
    ''' Class to score a git repository '''

    def __init__(self):
        self.git_score = 0
        self.commit_count = 0
        self.duplicate_commits = []
        self.merge_commits = []
        self.conventional_commits = False

    def get_all_commits(self, path):
        ''' Gets the git log for the repository
            :param path: The path to the git repository
        '''
        all_commits = os.popen("git -C " + path + " log --oneline").read()
        return all_commits

    def get_score(self, path):
        ''' Gets the git score for the repository '''

        all_commits = self.get_all_commits(path)
        commit_count = self.get_commit_count(all_commits)

        duplicate_commits = self.get_duplicate_commits(all_commits)
        merge_commits = self.get_merge_commits(all_commits)

        git_score = self.get_git_score(
            commit_count, duplicate_commits, merge_commits)

        print(f'Total commits: {str(commit_count)}')
        print(f'Duplicate commits: {str(len(duplicate_commits))}')
        print(f'Merge commits: {str(len(merge_commits))}')
        print(f'Conventional commits: {str(self.is_repo_following_conventionnal_commits(path))}')
        print(f'Git score: {str(git_score)}')

    def get_commit_count(self, all_commits):
        ''' Gets the total number of commits
            :param all_commits: The git log
        '''
        return len(all_commits.splitlines())

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
        commits = all_commits.splitlines()

        commits = [commit[8:] for commit in commits]

        for commit in commits:
            if commits.count(commit) > 1:
                duplicate_commits.append(commit)
        return duplicate_commits

    def get_merge_commits(self, all_commits):
        ''' Checks for merge commits in the git log
            :param all_commits: The git log
        '''
        merge_commits = []
        commits = all_commits.splitlines()

        for commit in commits:
            if "Merge" in commit:
                merge_commits.append(commit)
        return merge_commits

    def is_repo_following_conventionnal_commits(self, path):
        ''' Checks if the repository is following the conventional commits
                :param path: The path to the git repository
        '''
        commits = self.get_all_commits(path)
        commits = commits.splitlines()

        commits = [commit[8:] for commit in commits]

        for commit in commits:
            if re.match(r'^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test){1}(\([\w\-\.]+\))?(!)?: ([\w ])+([\s\S]*)', commit):
                continue
            else:
                return False
        return True
