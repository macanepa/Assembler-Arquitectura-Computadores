global error_list
error_list = []

def add_error(string,line=None):
    error_list.append((string,line))

def display_errors():

    print "Program couldn't compile succesfully, {} errors found:\n".format(str(len(error_list)))
    for error in error_list:
        if (error[1] != None):
            print (">: Error Line({}): - {}".format(error[1],error[0]))
        else:
            print (">: Error : - ({})".format(error[0]))

def get_num_errors():
    return len(error_list)

def print_error(string):
    print ">: Error : - ({})".format(string)