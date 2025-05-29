# BON: Bubu's Olympiad Navigator

## A problem database written in Python (inspired by VON)

This repository contains the scripts that are used by BON
inside the `bon-scripts/` directory. Furthermore, the raw
source code of the problems in the
database are present in `bon-db/`
for storage purposes. For anyone trying to
analyze how the scripts work, the
directory `bon-db/` can safely be ignored.

I have tried keeping this project as minimal as possible.
For searching problems using relevant keywords, I use
a plugin for neovim called [nvim-telescope][nvimtelescope]
which allows me to fuzzy find the problem
present in the database using relevant
keyword(s).

## Installation

> **_NOTE:_** Before you start, make sure you are using your
> own user and not
> the root one. You can check that by using `whoami`.

1. Run `cd $HOME` to go to your `HOME` directory.
   (This is essential for BON to work as intended.)

2. Run `git clone git@github.com:Bubu-Droid/bon.git` to
   clone the git repository in your `HOME` directory.

3. Add the `bon-scripts/` directory to your path.
   (Basically add `$HOME/bon/bon-scripts` to your
   `PATH` variable in `.zshrc` or its alternative.)

## Configuration

1. Most of the relevant variables are present in
   [bon.py][bonpy].
   The LaTeX templates that
   are used while adding, editing or previewing are
   in their respective
   [add.py][addpy],
   [edit.py][editpy],
   and [preview.py][previewpy]
   files respectively.

> It is STRONGLY recommended that you use my
> [bubu.sty][bubusty]
> file while using BON since the templates are based
> on [bubu.sty][bubusty]
> itself.

## Usage

Use `bon.py -h` to display the available options. As of
now (2025-05-29), the help command returns the following
output:

```
usage: bon.py [-h] [-a] [-e puid] [-p puid]

BON DB Manager

options:
  -h, --help          show this help message and exit
  -a, --add           Add a problem into the database
  -e, --edit puid     Edit a problem in the database
  -p, --preview puid  Preview the pdf of a problem in the database
```

More exposition about how the script works has been provided in
[this](#working-of-bon.py-script) section later on.

> **_NOTE:_** Just editing the TeX file won't make any change
> into the database automatically. The changes have to be manually
> copied to the `<PUID>.txt` file for the corresponding problem.
> I might automate this later on.

## DB file structure and a few more tools

- By default, the problems are stored using
  `.txt` extension inside the `bon-db/` directory
  after splitting the
  problem statement, first solution, second solution and so on.
  (A sample database file has been shown in the next section.)

- The `bon-scripts/` directory contains a few more scripts
  other than the ones dedicated for BON.
  - [niceasy.py][niceasypy] - This takes the asymptote code
    present in the clipboard, formats the code into a
    readable format and replaces the content of the clipboard
    with the formatted code.
  - [aops.py][aopspy] - This takes the TeX code present in the
    clipboard and formats that into AoPS compatible
    format. You can get a fair idea of what this script does
    by going through the script.
  - [puid_gen.py][puidgenpy] - This generates a random PUID
    which is used to store a problem into the database.

## An example of a file in the DB

```
desc: <short-description-of-the-problem-statement> (used for searching)
puid: <puid> (this is automatically added into the file once generated)
source: [<source(s)>] (used for searching)
tags: [<tag(s)>] (used for searching)
date: <yyyy-mm-dd> (this is automatically added into the file once generated)
hardness: <hardness> (additional parameter for searching)
---
\begin{problem}
  [\href{<url>}{<source>}] (this line is manually added)
  <problem-statement>
\end{problem}
---
\begin{soln}
  <solution>
\end{soln}
```

An example has been provided where the problem has multiple
solutions.

```
desc: find the value of 1 + 1
puid: DUMMY
source: [unknown, ohio]
tags: [ohioproblem, weird]
date: 2025-05-29
hardness: easy
---
\begin{problem}
  [\href{https://youtu.be/xvFZjo5PgG0?si=iPYyHeV4nMsyidra}{Ohio TST 2069/1}]
  Find the value of $1 + 1$.
\end{problem}
---
\begin{proof}[Solution 1.]
  \renewcommand{\qedsymbol}{$\blacksquare$}
  Using basic arithmetic, we find that thee answer is $2$.
\end{proof}
---
\begin{proof}[Solution 2.]
  \renewcommand{\qedsymbol}{$\blacksquare$}
  Using ohio algebra, the answer turns out to be $2$.
\end{proof}
```

## Working of [bon.py][bonpy] script

Assuming that the default variables are unchanged,
the working of the
script can be split into three cases as shown below.

- When `bon.py -a` is run, [puid_gen.py][puidgenpy]
  generates a random (and unique) PUID and
  creates a file by the name `<PUID>.txt` inside `bon-db/`
  directory using the bare template provided inside
  [add.py][addpy]. The script then creates another file
  at `/tmp/preview/bon-preview.tex` using the bare template
  as provided in [add.py][addpy]. After the TeX file is
  made, the script opens a new instance of `alacritty`
  and runs the command `latexmk -pdf -pvc bon-preview.tex`
  after changing directories. When the compilation is stopped,
  this new terminal instance is automatically killed.

- When `bon.py -e <PUID>` is run, the script searches the
  database for the file (errors aren't handled cuz I thought I'm
  not dumb enough to enter incorrect file name :P). Then it
  extracts the required part from the file `<PUID>.txt`
  and wraps it using the bare template present in
  [edit.py][editpy]. Finally, it launches the editor and
  starts the continuous compilation of `latexmk` similarly
  as in the previous case.

- When `bon.py -p <PUID>` is run, the script behaves similarly
  as the previous two cases except that no editor is launched and
  that the flags used with `latexmk` are `-pdf` and `-pv` only.

## LaTeX integration

For using the raw data from the files present in the database
in some other document, the library `pythontex` can be used.

In order to do so, add the following lines into your `*.sty`
file.

```latex
\RequirePackage{pythontex}
\setpythontexoutputdir{.}
\newcommand{\bubuprob}[1]{%
\py{print_bubuproblem(r"#1")}%
}
\newcommand{\bubuprobnonum}[1]{%
\py{print_bubuproblem_nonum(r"#1")}%
}
\newcommand{\bubusoln}[1]{%
\py{print_bubusoln(r"#1")}%
}
```

> [bubu.sty][bubusty] has everything configured by default.
> Only the `bon` option has to be passed while including the
> package,
> i.e., `\usepackage[bon]{bubu}`.

After adding the lines above, the following lines need to be
added into your TeX document right after `\begin{document}`.

```python
\begin{pycode}
import os
import sys
LOCAL_HOME = os.environ.get("HOME", "/home/bubu")
DB_SCRIPTS_PATH = os.path.join(LOCAL_HOME, "bon/bon-scripts/")
sys.path.insert(0, DB_SCRIPTS_PATH)
import bon
def print_bubuproblem(puid: str) -> None:
    db_file_path = os.path.join(bon.HOME, "bon/bon-db/", f"{puid}{bon.DB_FILE_EXT}")
    try:
        with open(db_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        db_sec = content.split(bon.SEPARATOR)
        return (db_sec[1])
    except Exception as e:
        return (f"[Error: {e}]")
def print_bubuproblem_nonum(puid: str) -> None:
    db_file_path = os.path.join(bon.HOME, "bon/bon-db/", f"{puid}{bon.DB_FILE_EXT}")
    try:
        with open(db_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        db_sec = content.split(bon.SEPARATOR)
        db_sec[1] = db_sec[1].replace("\\begin{problem}", "\\begin{problem*}")
        db_sec[1] = db_sec[1].replace("\\end{problem}", "\\end{problem*}")
        return (db_sec[1])
    except Exception as e:
        return (f"[Error: {e}]")
def print_bubusoln(puid: str) -> None:
    db_file_path = os.path.join(bon.HOME, "bon/bon-db/", f"{puid}{bon.DB_FILE_EXT}")
    try:
        with open(db_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        db_sec = content.split(bon.SEPARATOR)
        bon_inner_txt = "\n\\hrulebar\n".join(db_sec[2:])
        return (bon_inner_txt)
    except Exception as e:
        return (f"[Error: {e}]")
\end{pycode}
```

> If you use [bon.tex][bontex], then you can just add
> `\input{bon}` after `\begin{document}`.

This should be it.

For configuring `latexmk` to automatically compile the document
using `pythontex` when necessary, add the following lines into
your `latexmkrc`.

```perl
sub pythontex {
    system("pythontex --runall true \"$_[0]\"");
    system("touch \$(basename \"$_[0]\").pytxmcr");
    return;
}
add_cus_dep("pytxcode", "pytxmcr", 0, "pythontex");
```

> I suggest you add this to the local `latexmkrc`
> configuration file as adding this into the global `latexmkrc`
> unnecessarily slows down the compilation.

If you use an auxiliary directory for storing extraneous files
that are produced during compilation,
use `system("touch <dir-name>/\$(basename \"$_[0]\").pytxmcr");`
instead where `<dir-name` is the name of the auxiliary directory.

Thus the commands for adding data from the database should be like:

- `\bubuprob{<PUID>}` - When you want to add the problem statement
  with the problem number.
- `\bubuprobnonum{<PUID>}` - When you want to add the problem statement
  without the problem number.
- `\bubusoln{<PUID>}` - When you want to add the solution(s)
  for the corresponding problem.

---

### What was the motivation behind the name

Thought you'd never ask :upside_down_face:. The name has
basically been ripped off from
VON (vEnhance's Olympiad Navigator).

It was only after naming the script bon that I found out the
abbreviation fits well since my nickname starts with `B`. What
a cute coincidence. :laughing:

[bonpy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/bon.py
[addpy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/add.py
[editpy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/edit.py
[previewpy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/preview.py
[bubusty]: https://github.com/Bubu-Droid/dotfiles/blob/main/texmf/tex/latex/sty/bubu.sty
[niceasypy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/niceasy.py
[aopspy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/aops.py
[puidgenpy]: https://github.com/Bubu-Droid/bon/blob/main/bon-scripts/puid_gen.py
[bontex]: https://github.com/Bubu-Droid/dotfiles/blob/main/texmf/tex/latex/sty/bon.tex
[nvimtelescope]: https://github.com/nvim-telescope/telescope.nvim
