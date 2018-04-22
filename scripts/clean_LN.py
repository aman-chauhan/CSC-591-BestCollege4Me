import re
import sys

def main(filename):
    text=None
    with open("../raws/"+filename+".txt") as fp:
        text=list(filter(None,[line.strip() for line in fp.readlines()]))
    #arts=re.findall(r'(\s*)(\d+) of (\d+) DOCUMENTS(.*)',text)
    print(text)

if __name__=="__main__":
    main(sys.argv[1])
