import utilities

program_list = []
opcodes_list = []
label_dict = {}

out_list = []

# import available opcodes
opcodes_list = utilities.import_opcodes("opcode.txt")

# import program to compile
while True:
    try:
        # file_name= raw_input("Insert name of file: ")
        file_name = "program.txt"
        file = open(file_name, "r")
    except:
        print utilities.print_error("File not found!")
        continue
    break

(program_list, label_dict) = utilities.import_program("program.txt")



out_string = ""
error_counter = 0
for line in program_list:
    lit = 0
    flag = False

    # if content is label and doesn't exist then...
    if(not line[1].isdigit()):
        if (line[1] not in label_dict) and (line[1] != ""):
            utilities.print_error("Label {} doesn't exist".format(line[1]))
            continue

    for opcode in opcodes_list:

        if line[0] == opcode[0]:
            flag = True

            # Manage Labels
            if (line[1].isdigit()):
                lit = int(line[1])

            elif (not line[1].isdigit()) and (line[1]!= ""):
                lit = int(label_dict[line[1]])


            # print line
            # print opcode[0]+" - Cont: "+str(lit)
            lit = '{0:07b}'.format(int(lit))
            # print ">: {}_{}".format(str(lit),str(opcode[1]))+"\n"
            out_string += "{}_{}".format(str(lit),str(opcode[1]))+"\n"
            break

    if (not flag):
        print utilities.print_error("Instruction: '{}' doesn't exist!".format(line[0]),line[2])
        error_counter+=1


out_file = open(file_name.replace(".txt",".out"),"w")
out_file.write(out_string.strip())

if(error_counter) == 0:
    print "Program compiled succesfully!"
else:
    print "Program couldn't compile succesfully, {} errors found".format(str(error_counter))


