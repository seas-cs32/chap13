### chap13/rewrite.py
import os
import re
import sys

# Terminal colors
reset = '\033[0m'
red = '\033[31m'
blue = '\033[34m'

def get_fname(fullpath):
    '''Strip full pathname down to just the filename'''
    fname = re.search(r'(\w+\.py)$', fullpath).group(0)
    return fname


def process_traceback(lines, i):
    '''Highlight only the files in the current dir
       * Expects index i to point to the 'Traceback'
         line in the Python error output.
       * Returns a tuple:
        - list of function frames;
        - index i following the traceback block.
    '''
    i += 1  # skip 'Traceback' line
    stack = []  # stack frames
    cwd = os.getcwd()

    # Process each 'File' line in traceback
    while lines[i][:6] == '  File':
        # Define RE pattern and run match on current line
        p = r'  File "(?P<fname>.*)", line (?P<lnno>\d+), in (?P<fun>[\w<>]+)'
        m = re.match(p, lines[i])

        # Record stack frames for scripts in our current
        # directory; ignore frames in libraries.
        if m.group('fname')[:len(cwd)] == cwd:
            stack.insert(0, m.groupdict())

        i += 2
        assert i < len(lines)

    # i indicates where to continue processing in lines
    return (i, stack)


def print_stack(stack):
    '''Print stack of function frames when error occurred'''

    print(f"{red}**Call stack at ERROR**{reset}", file=sys.stderr)
    print(f"Function {blue}{stack[0]['fun']}{reset} was called from", file=sys.stderr)
    
    for i in range(1, len(stack)):
        print(' '*i, '\u219c', end=' ', file=sys.stderr)
        print(f"{blue}{stack[i]['fun']}{reset} in", end=" ", file=sys.stderr)
        fname = get_fname(stack[i]['fname'])
        print(f"{blue}{fname}{reset} on line", end=" ", file=sys.stderr)
        print(f"{blue}{stack[i]['lnno']}{reset}", end="", file=sys.stderr)

        if i + 1 != len(stack):
            print(", which was called from", file=sys.stderr)
        else:
            print("", file=sys.stderr)


def print_error(stack, err_msg):
    '''Print info about error'''
    
    # Print location of error with color highlights
    fname = get_fname(stack[0]['fname'])
    print(f"\n{red}**Hit an ERROR**{reset}", end=' ', file=sys.stderr)
    print(f"in {blue}{fname}{reset}", end=' ', file=sys.stderr)
    print(f"on {blue}line {stack[0]['lnno']}{reset}", file=sys.stderr)
    print(f"inside function {blue}{stack[0]['fun']}{reset}:", file=sys.stderr)
    print("", file=sys.stderr)

    # Print error line with context
    with open(stack[0]['fname']) as f:
        # Read entire script and split into lines
        script = f.read().split('\n')

        # Prepare to prepend script lines with line numbers
        lnno = int(stack[0]['lnno'])
        cols = len(str(lnno + 1))

        # Print error with context
        print(f'{(lnno-1):>{cols}}:', script[lnno-2], file=sys.stderr)
        #print(f'{red}{(lnno):>{cols}}: {lines[i - 1]}{reset}', file=sys.stderr)
        print(f'{red}{(lnno):>{cols}}: {script[lnno-1]}{reset}', file=sys.stderr)
        print(f'{(lnno+1):>{cols}}:', script[lnno], file=sys.stderr)
        print("", file=sys.stderr)

    # Print error itself
    print(err_msg, file=sys.stderr)
    print("", file=sys.stderr)

    # Print function call stack when error occurred, if
    # it is non-trivial.
    if len(stack) > 1:
        print_stack(stack)
        print("", file=sys.stderr)


def rewrite_emsg(e):
    '''Rewrite the standard Python error message'''
    lines = e.split('\n')
    i = 0

    if lines[0][:len('Traceback')] == 'Traceback':
        # Found a runtime error
        i, stack = process_traceback(lines, i)
    else:
        # Found a syntax error
        print(f'[rewrite]: This tool only rewrites runtime (not syntax) error messages')
        return

    # Verify "*Error" block comes next and print it
    assert re.match(r'.+Error:', lines[i]), \
           'No error after traceback'
    print_error(stack, lines[i])

    # Verify that there's nothing left in e
    i += 1
    assert i == len(lines) or lines[i] == '', \
           'Unexpected output at end of the error msg' 


def main():
    if len(sys.argv) == 1:
        # Test this script in this manner:
        #   python3 brokenscript.py 2> >(python3 rewrite.py)
        # which uses redirection magic.
        e = sys.stdin.read()
        rewrite_emsg(e)

    elif len(sys.argv) > 2:
        sys.exit('[rewrite]: Please provide a single error log')

    else:
        # Testing with an error log. Make sure that the log
        # was created in the current working directory (or
        # else os.getcwd does the wrong thing for us).
        with open(sys.argv[1]) as f:
            e = f.read()
            rewrite_emsg(e)

if __name__ == '__main__':
    main()
