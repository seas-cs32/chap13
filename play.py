### chap13/play.py
import re

p_string = input('Regex: ')
p = re.compile(p_string)

print(f"\nWhat strings are in the language of '{p_string}'?")

while True:
    candidate = input('String: ')
    if candidate == 'quit':
        break
    m = p.fullmatch(candidate)
    
    if m:
        print(f'{candidate}: Yes')
    else:
        print(f'{candidate}: No')