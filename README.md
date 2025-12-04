# BON: Bubu's Olympiad Navigator

## A problem database written in Python (inspired by VON)

BON is a problem database management system
written in Python after being inspired by
[Evan Chen][evan_chen]'s project,
[VON][von]. This repository
contains the source code of the scripts
involved in the working of this project.
It also contains a database which stores
the LaTeX code of problems and their
solutions that have been added by me.

- [bon/](bon) --- Contains the scripts that this
  project uses.
- [bon-db/](bon-db) --- Database where I store
  the code for problems, their solutions,
  and other relevant metadata.

I have tried keeping this project as minimal as possible.
For searching problems using relevant keyword(s), I use
a plugin for neovim called [nvim-telescope][nvimtelescope]
which allows me to fuzzy find the problem
present in the database.
However, I may add a dedicated
search functionality later on.

## Installation

> [!IMPORTANT]
> Before you start, make sure you are using your
> own user, not
> the root. You can check that by using `whoami`.

1. Change the current working directory
   to your `HOME` directory.
   (This is essential for BON to work as intended.)

2. Clone this git repository in your `HOME` directory.

3. Add the parent `bon/` directory to your PYTHONPATH.
   (Basically, add `export PYTHONPATH="$PYTHONPATH:$HOME/bon"`
   to your `.zshrc` or its alternative.)

4. Install the required Python packages that are
   listed in [requirements.txt](requirements.txt)

<!-- 4. Add the `bon/` directory to your path. -->
<!--    (Basically add `$HOME/bon/bon` to your -->
<!--    `PATH` variable in `.zshrc` or its alternative.) -->

## Configuration

1. Almost all of the
   relevant configuration variables
   can be found in [rc.py](bon/rc.py)
   The LaTeX templates that
   are used while adding, editing,
   or previewing can be found in the
   [templates](bon/templates/) directory.

> [!IMPORTANT]
> It is STRONGLY recommended that you use my
> [bubu.sty][bubusty]
> file while using BON since the templates are based
> on [bubu.sty][bubusty]
> itself. Moreover, if you are trying to integrate BON
> with LaTeX, the necessary environments
> are defined by default in [bon.tex][bontex] using
> `pythontex`.

## Usage

Use `python3 -m bon -h` to display the available options. As of
now (2025-12-04), the help command returns the following
output:

```text
usage: __main__.py [-h] [-a category] [-e puid] [-p puid]

BON DB Manager

options:
  -h, --help          show this help message and exit
  -a, --add category  add a problem into the database
  -e, --edit puid     edit a problem in the database
  -p, --preview puid  preview the pdf of a problem in the database
```

More exposition about how the script works has been provided in
[this](#working-of-bonpy-script) section later on.

> [!NOTE]
> After the introduction of
> [watcher.py](bon/watcher.py)
> (introduced in commit [`7c72c30`][7c72c30]),
> the script now automates
> the interaction between `bon-db/` and the LaTeX document
> that you are editing. Any change made in the file
> is automatically written into the database.
> Just ensure that
> you are using the `TEX_SEP` variable (default: `%---%`)
> to separate problem statement and individual
> solutions. Check the dummy LaTeX template given in
> [this](working-of-bonpy-script) section for more information.

By default, the problems are stored in
json format inside
[bon-db/](bon-db) directory
after separating the
problem statement and individual solutions.
(A sample database file has been shown in the next section.)

## An example of a file in the DB

```json
{
  "desc": "<short-description-of-the-problem-statement>" (used for searching),
  "puid": "<puid>" (this is automatically added into the file once generated),
  "source": ["<source(s)>"] (used for searching),
  "tags": ["<tag(s)>"] (used for searching),
  "date": "<yyyy-mm-dd>" (this is automatically added into the file once generated),
  "hardness": "<hardness>" (additional parameter for searching),
  "problem": "<problem-statement>",
  "solution": ["<solution(s)>"]
}
```

The following example illustrates the case where the problem
has multiple solutions. Moreover, if the value of
some source is kept empty (as seen below in case of
"NO-URL" key), then the source is printed
as plain text instead of a link.

```json
{
  "desc": "find the value of 1 + 1",
  "puid": "DUMMY",
  "source": [
    {
      "Ohio TST 2069/1": "https://youtu.be/xvFZjo5PgG0?si=iPYyHeV4nMsyidra"
    },
    {
      "NO-URL": ""
    }
  ],
  "tags": ["ohioproblem", "weird"],
  "date": "2025-05-29",
  "hardness": "hard",
  "problem": "\\begin{problem*}\n  Find the value of $1 + 1$.\n\\end{problem*}",
  "solution": [
    "\\begin{soln}\n  Using basic arithmetic, we find that the answer is $2$.\n\\end{soln}",
    "\\begin{soln}\n  Using Ohio algebra, the answer turns out to be $2$.\n\\end{soln}"
  ]
}
```

The corresponding LaTeX code generated
for editing the above json file is:

```latex
\documentclass[12pt]{article}

\usepackage[min]{bubu}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\title{BON PREVIEW}
\author{Avigyan Chakraborty}
\date{\today}

\begin{document}

\section*{DUMMY (\href{https://youtu.be/xvFZjo5PgG0?si=iPYyHeV4nMsyidra}{Ohio TST 2069/1}, NO-URL)}

%---%
\begin{problem*}
  Find the value of $1 + 1$.
\end{problem*}
%---%
\begin{soln}
  Using basic arithmetic, we find that the answer is $2$.
\end{soln}
%---%
\begin{soln}
  Using Ohio algebra, the answer turns out to be $2$.
\end{soln}
%---%

\end{document}
```

## Working of BON

Assuming that the default variables are unchanged,
the working of the
script can be split into the following cases
as shown below:

- When `python3 -m bon -a <CATEGORY>`
  is run, [puid.py](bon/puid.py)
  generates a random (and unique) PUID
  which is then piped into [edit.py](bon/edit.py).
  Then a file with the name `<PUID>.json`
  is created inside `bon-db/<CATEGORY>/`
  directory and an empty template
  is written into it.
  The script then creates another file
  at `/tmp/preview/bon-preview.tex`
  using the template
  provided in
  [templates/add.txt](bon/templates/add.py).
  After the LaTeX document is
  made, the script opens a new instance of `alacritty`
  and runs the command `latexmk -pdf -pvc bon-preview.tex`
  after changing directories. While this is being done,
  the script also fires up an
  Observer instance which is responsible for
  monitoring and
  automatically writing changes into the database when the
  LaTeX document is updated. When the compilation is stopped,
  this new terminal instance is automatically killed.
  When the editor is quit, the Observer is also stopped.

> [!NOTE]
> The following categories are available as of now:
>
> - seq --- Sequences and series
> - cont --- Continuity
> - diff --- Differentiability
> - int --- Integration
> - geo --- Geometry
> - nt --- Number theory
> - combi --- Combinatorics
> - alg --- Algebra
>
> Using any other category results in printing
> an appropriate message along with a list of
> all the available valid categories followed by the
> termination of the script.

- When `python3 -m bon -e <PUID>` is run,
  the script searches for `<PUID>.json`
  recursively through the database.
  The current structure of the database is as follows:

  ```text
    /home/bubu/bon/bon-db
    ├── alg
    ├── calculus
    │   ├── cont
    │   ├── diff
    │   ├── int
    │   └── seq
    ├── combi
    ├── geo
    └── nt
  ```

If the file is not found, it prints an appropriate
message and the script is terminated.
Otherwise, it
extracts the required data from `<PUID>.json`
and wraps it using the template present in
[templates/edit.txt](bon/templates/edit.py).
Finally, it launches the editor and
starts the continuous compilation of
`latexmk`, analogous to that in the previous case.

- When `python3 -m bon -p <PUID>` is run,
  the script behaves similarly
  as the previous two cases except that no editor is
  launched and
  that the flags used with `latexmk` are `-pdf` and `-pv` only.

- The [bon/](bon) directory contains a few more scripts
  other than the ones mentioned above. Here is a brief
  description of each of those scripts:
  - [niceasy.py](bon/niceasy.py) --- This takes the asymptote
    code present in the clipboard, formats the code into a
    readable format, and replaces the content of the
    clipboard with the formatted code.
  - [aops.py](bon/aops.py) --- This takes the LaTeX code present in the
    clipboard and formats that into AoPS compatible
    format. You can get a fair idea of what this script does
    by going through the script.
  - [puid.py](bon/puid.py) --- Its functionalities include
    generating a random PUID, validating if a PUID
    is unique, and fetching the path of a file using its
    PUID.
  - [watcher.py](bon/watcher.py) --- This watches the
    LaTeX document that is being edited. Every time
    the document is updated, it fires up a function which
    writes the new changes into the database.

## LaTeX integration

The `pythontex` library can be used to include the LaTeX
code of a file from the database in other LaTeX documents.

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

> [!TIP]
> [bubu.sty][bubusty] has everything configured by default.
> Only the `bon` option has to be passed while including the
> package,
> that is, `\usepackage[bon]{bubu}`.

After adding the lines above, download [bon.tex][bontex]
and move the file into your working directory.
Then add the line
`\input{bon}` right after `\begin{document}`.

This should be it.

For configuring `latexmk` to automatically
compile the document using `pythontex` whenever necessary,
add the following lines into your `latexmkrc`.

```perl
sub pythontex {
    system("pythontex --runall true \"$_[0]\"");
    system("touch \$(basename \"$_[0]\").pytxmcr");
    return;
}
add_cus_dep("pytxcode", "pytxmcr", 0, "pythontex");
```

> [!TIP]
> I suggest you add this to the local `latexmkrc`
> configuration file as adding this into the global `latexmkrc`
> unnecessarily slows down the compilation.

If you use an auxiliary directory for storing
temporary build files
that are produced during compilation,
use `system("touch <dir-name>/\$(basename \"$_[0]\").pytxmcr");`
instead where `<dir-name>` is the name of the auxiliary directory.

The commands for adding problem/solution(s)
from the database should be like:

- `\bonincludle{problem}{<PUID>}` ---
  When you want to add the problem statement.
- `\boninclude{soln}{<PUID>}` ---
  When you want to add the solution(s)
  for the corresponding problem.

Here, you can also use
`problem`, `problem*`, `exercise`, `exercise*`,
`example`, `exmaple*`, `soln`, `solution`
as the first argument in
`\boninclude{}{}`. Furthermore, `soln` and `solution` are
equivalent, and hence, interchangeable.

---

### What was the motivation behind the name

Thought you'd never ask :upside_down_face:. The name has
basically been ripped off from
VON (vEnhance's Olympiad Navigator).

It was only after naming the script bon that I found out the
abbreviation fits well since my nickname starts with `B`. What
a cute coincidence. :laughing:

[bubusty]: https://github.com/Bubu-Droid/dotfiles/blob/main/texmf/tex/latex/sty/bubu.sty
[bontex]: https://github.com/Bubu-Droid/dotfiles/blob/main/texmf/tex/latex/sty/bon.tex
[nvimtelescope]: https://github.com/nvim-telescope/telescope.nvim
[7c72c30]: https://github.com/Bubu-Droid/bon/commit/7c72c30af36b77ba13efb63b2d32e6d3d21e7c62
[evan_chen]: https://github.com/vEnhance
[von]: https://github.com/vEnhance/von
