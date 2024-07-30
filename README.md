This directory contains everything needed for
**Chapter 13 (Rewrite the Error Messages)** in
[*Computational Thinking and Problem Solving (CTPS)*](https://profsmith89.github.io/ctps/ctps.html)
by Michael D. Smith.

`broken.py`: A script with a straightforward error.

`out*.txt`: Captures of the different outputs from `broken.py`.

`play.py`: A script that allows you to explore the strings in a
language defined by a regular expression.

`rewrite.py`: A script that uses the regular-expression library to
rewrite a script's stderr output.

`python32.py`: A shim around `python3` that allows us to use
`rewrite.py` to modify the format of its error messages.
