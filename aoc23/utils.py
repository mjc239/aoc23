def read_input(day):
    filename = f"../data/day{day}.txt"
    f = open(filename, "r")
    filestring = f.read()
    return filestring.split('\n')