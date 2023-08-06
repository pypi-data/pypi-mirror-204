# FileWiz

I keep files named and organized in a certain way in DropBox. This tool names new files correctly and puts them in the right directory.

## Installation

It's best to install using `pipx`. See [the pipx site](https://pypa.github.io/pipx/) if you need it. Then:

```bash
pipx install filewiz
```

## Usage

The directory pattern for account documents is:

```
~/Dropbox/accounts/<year>/<account>/<date>-<part>.<extension>
```

Where:

- `year` is the year of the document, typically from the date
- `account` is the name of the account, all lower case, hyphen separated
- `date` is the date on the document in `YYYYMMDD` format
- `part` is the textual part of the name of the document, often starting with the account name, all lower case, hyphen separated
- `extension` is the original filename extension, often `pdf`

I have my browsers etc. set to download new files to Desktop, then it's easy to run FileWiz on a file on the desktop using tab completion.

```
filewiz ~/Desktop/123456789SomeFileIDownloaded.pdf
```

FileWiz will ask a series of questions, then move the file.

Note the `part` supports tab-completion, where it looks up all the files previously stored under that account, in any year. So it's easy to reproduce names of periodic files such as financial statements or invoices.

## Credits

Copyright (C) 2023 by Francis Potter. Licensed under the MIT license.

Logo shown on GitLab is by [vectorsmarket15](https://www.flaticon.com/free-icon/folders_2821739?term=file&page=1&position=15&origin=search&related_id=2821739#:~:text=have%20to%20attribute-,vectorsmarket15,-Every%20time%20you)

