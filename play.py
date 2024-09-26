### chap13/play.py
"""A short script that allows you to test your understanding
   of different REs. You input a RE at the first prompt, and
   then you provide candidate strings at the second. If the
   string is part of the language described by the RE (i.e.,
   the string matches the pattern), the script returns
   True and False otherwise."""
import re

try:
    # Grab the user's RE and try to compile it
    p_string = input('RE: ')
    p = re.compile(p_string)

except re.error as e:
    print(f"RE compile failed: {e}")
          
else:
    print(f"\nWhat strings are in the language of '{p_string}'?")

    while True:
        candidate = input('String: ')
        if candidate == 'quit':
            break

        # Check the string against the RE
        m = p.fullmatch(candidate)
        if m:
            print(f'{candidate}: Yes')
        else:
            print(f'{candidate}: No')
