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
            "-g", "--git-repo", help="The path to the git repository folder to score")
        arg_parser.add_argument(
            "-r", "--remote", help="The url for the remote github repository to score")
        args = arg_parser.parse_args()

        if self.has_local_repo(args):
            self.check_if_valid(args.git_repo)
        elif self.has_remote_repo(args):
            self.get_remote_repo(args.remote)
        else:
            print("No git repository path provided")

    def has_remote_repo(self, args):
        ''' Checks if the remote repo arg is provided
            :param args: The command line args
        '''
        return hasattr(args, 'remote') and args.remote is not None

    def has_local_repo(self, args):
        ''' Checks if the local repo arg is provided
            :param args: The command line args
        '''
        return hasattr(args, 'git_repo') and args.git_repo is not None

    def get_remote_repo(self, remote):
        ''' Gets the remote repository
            :param remote: The remote repository url
        '''
        os.system("mkdir temp")
        os.chdir("temp")
        os.system("git clone " + remote)
        self.check_if_valid(remote.split('/')[-1].split('.')[0])

    def check_if_valid(self, path):
        ''' Check if the arg is a valid git repository
            :param path: The path to the git repository
        '''
        if os.path.isdir(path):
            if self.is_git_repo(path):
                self.gitscore.get_score(path)
                self.delete_temp_folder()
            else:
                print("Path is not a git repository")
        else:
            print("Path does not exist")

    def is_git_repo(self, path):
        ''' Checks if the path is a git repository
            :param path: The path to the git repository
        '''
        return os.path.isdir(os.path.join(path, '.git'))

    def delete_temp_folder(self):
        ''' Deletes the temp folder '''
        os.chdir("..")
        os.system("rmdir /s /q temp")
