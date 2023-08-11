''' App class '''
import argparse
import os

from gitscore.gitscore import GitScore


class App:
    ''' Class to score a git repository '''

    def __init__(self):
        self.gitscore = GitScore()

    def main(self):
        ''' Main method '''
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            "-g", "--git-repo", help="The path to the git repository to score")
        args = arg_parser.parse_args()
        if hasattr(args, 'git_repo') and args.git_repo is not None:
            self.check_if_valid(args.git_repo)
        else:
            print("No git repository path provided")

    def check_if_valid(self, path):
        ''' Check if the arg is a valid git repository
            :param path: The path to the git repository
        '''
        if os.path.isdir(path):
            if self.is_git_repo(path):
                self.gitscore.get_score(path)
            else:
                print("Path is not a git repository")
        else:
            print("Path does not exist")

    def is_git_repo(self, path):
        ''' Checks if the path is a git repository
            :param path: The path to the git repository
        '''
        return os.path.isdir(os.path.join(path, '.git'))
