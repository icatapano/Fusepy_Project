filename = "./fusemount/geiger"
file = open(filename, 'r')

if file.mode == 'r':
    toread = file.read()
    print(toread)
