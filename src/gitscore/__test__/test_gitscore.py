import unittest
from unittest.mock import patch
from gitscore.gitscore import GitScore

class TestGitScore(unittest.TestCase):

    @patch('gitscore.gitscore.requests.get')
    def test_get_repo_informations_valid(self, mock_get):
        mock_response = {
            'name': 'test_repo',
            'description': 'A test repository',
            'language': 'Python',
            'owner': {'login': 'test_owner'}
        }
        mock_get.return_value.json.return_value = mock_response
        git_score = GitScore()
        result = git_score.get_repo_informations('https://github.com/test_owner/test_repo')
        self.assertEqual(result, mock_response)

    @patch('gitscore.gitscore.requests.get')
    def test_get_repo_informations_invalid(self, mock_get):
        mock_response = None
        mock_get.return_value.json.return_value = mock_response
        git_score = GitScore()
        result = git_score.get_repo_informations('https://github.com/nonexistent_owner/nonexistent_repo')
        self.assertIsNone(result)

    @patch('gitscore.gitscore.requests.get')
    def test_get_all_commits(self, mock_get):
        mock_response = [
            {'commit': {'message': 'Commit 1'}},
            {'commit': {'message': 'Commit 2'}}
        ]
        mock_get.return_value.json.side_effect = [mock_response, []]
        git_score = GitScore()
        result = git_score.get_all_commits('test_owner', 'test_repo')
        self.assertEqual(result, ['Commit 1', 'Commit 2'])

    def test_get_commit_count(self):
        git_score = GitScore()
        result = git_score.get_commit_count(['Commit 1', 'Commit 2'])
        self.assertEqual(result, 2)

    def test_get_git_score(self):
        git_score = GitScore()
        result = git_score.get_git_score(10, ['Duplicate 1', 'Duplicate 2'], ['Merge 1', 'Merge 2'])
        self.assertEqual(result, 'D-')

    def test_get_letter_grade(self):
        git_score = GitScore()
        result = git_score.get_letter_grade(85)
        self.assertEqual(result, 'B')

    def test_get_duplicate_commits(self):
        git_score = GitScore()
        result = git_score.get_duplicate_commits(['Commit 1', 'Commit 2', 'Commit 1', 'Commit 3'])
        self.assertEqual(result, ['Commit 1', 'Commit 1'])

    def test_get_merge_commits(self):
        git_score = GitScore()
        result = git_score.get_merge_commits(['Commit', 'Merge 1', 'Merge 2', 'Commit'])
        self.assertEqual(result, ['Merge 1', 'Merge 2'])

    def test_is_repo_following_conventional_commits_true(self):
        git_score = GitScore()
        commits = [
            'feat: add new feature',
            'fix: fix a bug',
            'chore: update build process',
        ]
        result = git_score.is_repo_following_conventionnal_commits(commits)
        self.assertTrue(result)

    def test_is_repo_following_conventional_commits_false(self):
        git_score = GitScore()
        commits = [
            'feat: add new feature',
            'random message',
            'chore: update build process',
        ]
        result = git_score.is_repo_following_conventionnal_commits(commits)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
