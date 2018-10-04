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
        # file_name = "P1.txt"
        # file_name = "producto_punto.txt"
        file = open(file_name, "r")
    except:
        print error_manager.print_error("File '{}' not found!".format(file_name))
        continue
    break

lines_info = []
(program_list, label_dict, data_dict, lines_info) = utilities.import_program(file_name)

# use_offset separa la memoria de DATA y de CODE
use_offset = False

n_out = 0
out_string = ""
error_counter = 0



for line in program_list:
    lit = 0
    flag = False
    # print line
    # if content is label and doesn't exist then...
    if(not line[1].rstrip('D').isdigit()):


        if (line[0][0] == "J" or (line[0].split(" ")[0] != "CMP" and line[0].split(" ")[0][0] == "C")):
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

                # Error in case the DIR literal is larger than 8 bit
                if (line[1][-1] == 'D'):
                    if (int(line[1].strip('D'))<0) or (int(line[1].strip('D'))>255):
                        error_manager.add_error("DIR out of range!", line[2])

                # Error in case the literal is larger than 8 bit
                else:
                    if (int(line[1])<-128) or (int(line[1])>127):
                        error_manager.add_error("Literal out of range!", line[2])


                if(line[1] != ''):
                    if(line[1][-1] == 'D'):
                        if(use_offset):
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




            lit = '{0:07b}'.format(int(lit))

            list = opcode[1].split("\\n")
            for opc in list:
                out_string += "{}_{}".format(str(lit),str(opc))+"\n"
            n_out+=1
            break

    if (not flag):
        error_manager.add_error("Instruction: '{}' doesn't exist!".format(line[0]),line[2])






n_data = 0
n_code = 0

n_data = data_dict.__len__()
n_code = program_list.__len__()

if(error_manager.get_num_errors() == 0):

    mem_file = open(file_name.replace(".txt", ".mem"), "w")
    write_data = utilities.sort_data(data_dict)

    for data in write_data:
        directory = int(data[0])
        data = int(data[1])

        # MOV A,DATA
        mem_file.write("{0:07b}_".format(data) + ("{}\n".format("0000010")))

        # MOV DIR,A
        mem_file.write("{0:07b}_".format(directory) + ("{}\n".format("0100111")))


    mem_file.close()

    out_file = open(file_name.replace(".txt", ".out"), "w")
    out_file.write(out_string.strip())
    out_file.close()



    print "Program compiled succesfully!"
    print "# Lines of Data: {}".format(str(lines_info[0]))
    print "# Lines of Code: {}".format(str(lines_info[1]))
    print "# Lines of .out: {}".format(str(n_out))
else:
    error_manager.display_errors()
