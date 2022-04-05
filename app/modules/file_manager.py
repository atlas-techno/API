def create_file(name="main.tf"):
    f = open(f'{name}',mode="a")
    return name

def edit_file(file):
    return open(f'{file}',mode="a")
    
def dictify(object):
    return object.dict()
    