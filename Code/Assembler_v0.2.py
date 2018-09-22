import utilities

program_list = []
opcodes_list = []
label_dict = {}
data_dict = {}

out_list = []

# import available opcodes
opcodes_list = utilities.import_opcodes("opcode.txt")

# import program to compile
while True:
    try:
        # file_name= raw_input("Insert name of file: ")
        file_name = "program2.txt"
        file = open(file_name, "r")
    except:
        print utilities.print_error("File not found!")
        continue
    break

(program_list, label_dict, data_dict) = utilities.import_program(file_name)




n_out = 0
out_string = ""
error_counter = 0

memory_data_index = 0
# Assign the variables to memory
# for variable in data_dict:
    # print variable, data_dict[variable]
    # data_dict[variable][0]=memory_data_index
    # print variable, data_dict[variable]
    # memory_data_index+=1
print data_dict


for line in program_list:
    lit = 0
    flag = False

    # if content is label and doesn't exist then...
    if(not line[1].isdigit()):
        if (line[1] not in label_dict) and (line[1] != ""):
            utilities.print_error("Label {} doesn't exist".format(line[1]))
            error_counter+=1
            continue

    for opcode in opcodes_list:

        if line[0] == opcode[0]:
            flag = True

            # Manage Labels
            if (line[1].isdigit()):
                lit = int(line[1])

            elif (not line[1].isdigit()) and (line[1]!= ""):
                lit = int(label_dict[line[1]])


            # Error in case the literal is larger than 8 bit
            if (lit > 256):
                utilities.print_error("Literal out of range")
                error_counter+=1


            print line
            # print opcode[0]+" - Cont: "+str(lit)
            lit = '{0:07b}'.format(int(lit))
            # print ">: {}_{}".format(str(lit),str(opcode[1]))+"\n"
            out_string += "{}_{}".format(str(lit),str(opcode[1]))+"\n"
            n_out+=1
            break

    if (not flag):
        print utilities.print_error("Instruction: '{}' doesn't exist!".format(line[0]),line[2])
        error_counter+=1


out_file = open(file_name.replace(".txt",".out"),"w")
out_file.write(out_string.strip())

n_data = 0
n_code = 0
# n_out = 0

for line in file:
    n_code+=1






if(error_counter) == 0:
    print "Program compiled succesfully!"
    print "# Lines of Data: {}".format(str(n_data))
    print "# Lines of Code: {}".format(str(n_code))
    print "# Lines of .out: {}".format(str(n_out))
else:
    print "Program couldn't compile succesfully, {} errors found".format(str(error_counter))


