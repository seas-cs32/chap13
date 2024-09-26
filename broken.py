### chap13/broken.py
import re

def f_undef_name():
    print(undef_name)

def main():
    # Process two strings in similar, but not quite
    # the same manner.

    s1 = 'this is a test'
    p = re.compile('[a-z]+', re.IGNORECASE)
    wlist = p.findall(s1)
    print(wlist)
    
    s2 = 'This is another test.'
    wlist = re.findall(r'[a-z]+', s2)
    print(wlist)
    
    f_undef_name()

if __name__ == '__main__':
    main()