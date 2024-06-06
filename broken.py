### chap13/broken.py
import re

def f_undef_name():
    print(undef_name)

def main():
    s1 = 'this is a test'
    s2 = 'This is another test.'

    # Process these strings in similar, but not quite
    # the same manner.

    p = re.compile('[a-z]+', re.IGNORECASE)
    print(p.findall(s1))
    
    wlist = re.findall(r'[a-z]+', s2)
    print(wlist)
    
    f_undef_name()

if __name__ == '__main__':
    main()