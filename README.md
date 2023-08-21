# GitScore

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/TommyRiquet/GitScore/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/TommyRiquet/GitScore.svg)](https://github.com/TommyRiquet/GitScore/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/TommyRiquet/GitScore.svg)](https://github.com/TommyRiquet/GitScore/pulls)

GitScore is a Python-based tool that evaluates GitHub repositories using various criteria, such as duplicate commits, merges, and adherence to conventional commit messages.

![ui](https://raw.githubusercontent.com/TommyRiquet/GitScore/main/docs/ui.png)

## Features

- Analyze GitHub repositories based on commit quality.
- Detect duplicate commits and non-standard commit messages.
- Evaluate merge frequency and adherence to best practices.

## Requirements

- Python 3.9 or later
- See the `requirements.txt` file for a list of dependencies.

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

Run the GitScore script by providing the path to the repository you want to evaluate:

```bash
python src/gitscore.py -g path/to/repo
```

## Contribution

Contributions to GitScore are welcome and encouraged! If you find any issues or have improvements in mind, feel free to open an issue or submit a pull request.

## License

GitScore is released under the MIT License.

## Contact

For questions or support, you can reach out to us on GitHub Issues.