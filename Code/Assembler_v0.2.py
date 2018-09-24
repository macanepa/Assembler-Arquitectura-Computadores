import utilities
import error_manager

program_list = []
opcodes_list = []
label_dict = {}
data_dict = {}

# import available opcodes
opcodes_list = utilities.import_opcodes("opcode.txt")

# import program to compile
while True:
    try:
        file_name= raw_input("Insert name of file: ")
        # file_name = "P3.txt"
        file = open(file_name, "r")
    except:
        print error_manager.print_error("File '{}' not found!".format(file_name))
        continue
    break

(program_list, label_dict, data_dict) = utilities.import_program(file_name)


n_out = 0
out_string = ""
error_counter = 0



for line in program_list:
    lit = 0
    flag = False

    # if content is label and doesn't exist then...
    if(not line[1].rstrip('D').isdigit()):



        if (line[0][0] == "J"):
            if (line[1] not in label_dict) and (line[1] != ""):
                error_manager.add_error("Label: '{}' doesn't exist!".format(line[1]),line[2])
                continue
        elif (line[1] not in data_dict) and (line[1] != ""):
            error_manager.add_error("Variable: '{}' not declared!".format(line[1]),line[2])


    for opcode in opcodes_list:

        if line[0] == opcode[0]:
            flag = True

            # Manage Labels
            if (line[1].strip('D').isdigit()):
                lit = int(line[1].strip('D'))

                if(line[1] != ''):
                    if(line[1][-1] == 'D'):
                        lit+= data_dict.__len__()
            elif (not line[1].strip('D').isdigit()) and (line[1]!= ""):
                try:
                    lit = int(label_dict[line[1]])
                except:
                    try:
                        # lit = dir of variable
                        lit = int(data_dict[line[1]][0])
                    except:
                        None



            # Error in case the literal is larger than 8 bit

            if (lit > 256):
                error_manager.add_error("Literal out of range!",line[2])
            lit = '{0:07b}'.format(int(lit))
            out_string += "{}_{}".format(str(lit),str(opcode[1]))+"\n"
            n_out+=1
            break

    if (not flag):
        error_manager.add_error("Instruction: '{}' doesn't exist!".format(line[0]),line[2])


out_file = open(file_name.replace(".txt",".out"),"w")


write_data = utilities.sort_data(data_dict)
print write_data

for data in write_data:
    out_file.write("MEM_DIR: {}".format(int(data[0])) +  (" Value: {0:07b}\n".format(int(data[1]))))



out_file.write("\n"+out_string.strip())

n_data = 0
n_code = 0

for line in file:
    n_code+=1



if(error_manager.get_num_errors() == 0):


    print "Program compiled succesfully!"
    print "# Lines of Data: {}".format(str(n_data))
    print "# Lines of Code: {}".format(str(n_code))
    print "# Lines of .out: {}".format(str(n_out))
else:
    error_manager.display_errors()

print data_dict
