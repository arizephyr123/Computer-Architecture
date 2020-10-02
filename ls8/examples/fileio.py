import sys

if len(sys.argv) != 2:
    print('remember to pass in second filename as arg')
    print('usage: python3 fileio.py <secon_file_name>')
    sys.exit()

try:
    # with open('print8.ls8') as f: # hard-coded file
    with open(sys.argv[1]) as f:
        for line in f:
            # print(line)
            # parse the file lines to isolate the binary
            possible_num = line[:line.find('#')]
            # print(possible_num)
            if possible_num == '':
                continue # skip to next interation of loop
                
            regular_int = int(possible_num, 2)
            # int(variable,       base num  ^)
            print(regular_int)



    print('f.closed ->', f.closed)

except FileNotFoundError:
    print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
    sys.exit()
