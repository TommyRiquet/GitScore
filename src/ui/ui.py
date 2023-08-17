''' UI class for the application '''
import os
import PySimpleGUI as sg

from gitscore.gitscore import GitScore


class UI:
    ''' UI class '''

    def __init__(self):
        sg.change_look_and_feel('DarkBlue')
        sg.set_options(font=("Poppins", 14))
        self.window = sg.Window("GitScore", self.get_layout(),
                                icon=os.path.join(os.path.dirname(__file__), '../assets/icon.ico'))

        self.gitscore = GitScore()
        self.git_repo_info = None

    def get_layout(self):
        ''' Layout method '''

        input_layout = [
            [
                sg.Text('GitScore', font=('Poppins', 20),
                        expand_x=True, justification='center')
            ],
            [
                sg.Text("https://github.com/", size=(14, 1)),
                sg.InputText(key="-URL-"),
            ],
            [
                sg.Button("Get Score", size=(60, 1),
                          bind_return_key=True, key="-GET_GIT_SCORE-")
            ],
        ]

        git_repo_informations = [
            [
                sg.Text("Repo name: ", expand_x=True, font=('Poppins', 11)),
                sg.Text("TESt", key="-REPO_NAME-", font=('Poppins', 11))
            ],
            [
                sg.Text("Language: ", expand_x=True, font=('Poppins', 11)),
                sg.Text("TEST", key="-REPO_LANGUAGE-", font=('Poppins', 11))
            ],
            [
                sg.Text("Owner: ", expand_x=True, font=('Poppins', 11)),
                sg.Text("TEST", key="-OWNER_NAME-", font=('Poppins', 11))
            ],
            [
                sg.Text("Description: ", expand_x=True, font=('Poppins', 11)),
                sg.Text("TESTTESTTESTTEST TESTTESTTEST TESTTEST TESTTESTTESTTESTTESTTEST", key="-REPO_DESCRIPTION-",
                             font=('Poppins', 11), size=(20, 3))
            ]
        ]

        git_repo_score = [
            [
                sg.Text("Total commits: ", expand_x=True,
                        font=('Poppins', 11)),
                sg.Text("100", key="-TOTAL_COMMITS-", font=('Poppins', 11)),
            ],
            [
                sg.Text("Duplicate commits: ",
                        expand_x=True, font=('Poppins', 11)),
                sg.Text("100", key="-DUPLICATE_COMMITS-",
                        font=('Poppins', 11)),
            ],
            [
                sg.Text("Merge commits: ", expand_x=True,
                        font=('Poppins', 11)),
                sg.Text("100", key="-MERGE_COMMITS-", font=('Poppins', 11)),
            ],
            [
                sg.Text("Conventional commits: ",
                        expand_x=True, font=('Poppins', 11)),
                sg.Text("100", key="-CONVENTIONAL_COMMITS-",
                        font=('Poppins', 11)),
            ],
            [
                sg.Text("Git score: ", expand_x=True, font=('Poppins', 11)),
                sg.Text("100", key="-GIT_SCORE-", font=('Poppins', 11))
            ]
        ]

        git_repo_layout = [
            [sg.Frame('Informations', git_repo_informations,
                      vertical_alignment='top', expand_x=True, element_justification='center')],
            [sg.Frame('Score', git_repo_score, expand_x=True, vertical_alignment='top', element_justification='center')]
        ]

        layout = [
            [
                input_layout,
                git_repo_layout
            ]
        ]

        return layout

    def main(self):
        ''' Main method '''

        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            if event == "-GET_GIT_SCORE-":
                url = values["-URL-"]

                if url == "":
                    sg.Popup("Please enter a url")
                else:
                    self.git_repo_info = self.gitscore.get_score(url)
                    if self.git_repo_info is None:
                        sg.Popup("Repository not found")
                    else:
                        self.update_repo_info()

    def update_repo_info(self):
        ''' Updates the repo info displayed on the UI'''

        self.window["-REPO_NAME-"].update(self.git_repo_info['repo_name'])
        self.window["-REPO_DESCRIPTION-"].update(
            self.git_repo_info['repo_description'])
        self.window["-REPO_LANGUAGE-"].update(
            self.git_repo_info['repo_language'])
        self.window["-OWNER_NAME-"].update(self.git_repo_info['owner_name'])
        self.window["-TOTAL_COMMITS-"].update(
            self.git_repo_info['total_commits'])
        self.window["-DUPLICATE_COMMITS-"].update(
            len(self.git_repo_info['duplicate_commits']))
        self.window["-MERGE_COMMITS-"].update(
            len(self.git_repo_info['merge_commits']))
        self.window["-CONVENTIONAL_COMMITS-"].update(
            self.git_repo_info['conventional_commits'])
        self.window["-GIT_SCORE-"].update(self.git_repo_info['git_score'])
