def read_input(day):
    with open(f"../data/day{day}.txt", 'r') as f:
        filestring = f.read()
    
    return filestring.split('\n')