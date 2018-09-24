def print_error(string_error,line_index=""):


    if (line_index != ""):
        print ">: Error Line:{} - ({})".format(line_index,string_error)
    else:
        print ">: Error:{} - ({})".format(line_index, string_error)

def import_opcodes(file_name):
    file = open(file_name, "r")
    opcodes_list = list()
    for line in file:
        opcodes_list.append(tuple(list(line.strip().split('-'))))
    file.close()
    return opcodes_list

def import_program(file_name):

    program_list = list()
    data_dict = dict()
    memory_data_index = 0

    load_data = False
    label_list = dict()




    # literal for the operation
    content = ""


    # file_name = raw_input("Ingrese el nombre del archivo: ")
    file = open(file_name,"r")

    pc = 1
    for line in file:
        content = ""
        # print line.strip()
        out_line = line.strip().replace("\t","").rstrip()
        out_line = out_line.replace("  "," ")
        # remove comments
        if (out_line.__contains__("//")):
            index_comment = line.index("//")
            out_line = line[:index_comment]

        while (out_line.endswith(" ")):
            out_line = out_line[:-1]

        while (out_line.startswith(" ")):
            out_line = out_line[2:]
        # print out_line


        # continue if the line is empty
        if (out_line == ""):
            pc+=1
            continue

        # check if line contain a label
        if (out_line.__contains__(':')):
            index_label = out_line.index(":")
            label = out_line[:index_label]

            if (label == "DATA"):
                load_data = True
            else:
                load_data = False

            label_list[label] = pc



            if (out_line[index_label+1:] != ""):
                out_line = out_line[index_label+1:]
            else:
                pc+=1
                continue


        # Replace content of a dir with DIR
        if ("(" in out_line) and (")" in out_line) and ("(A)" not in out_line) and ("(B)" not in out_line):
            index_s = out_line.index("(")
            index_f = out_line.index(")")

            # if it is hex
            if (out_line[index_s+1] == "#"):
                content = str(int(out_line[index_s + 2:index_f],16))+"D"
            elif ((out_line[index_s + 1:index_f]).isdigit()):
                content =str((out_line[index_s + 1:index_f]))+"D"
            else:
            #     if not, this means its a variable
                content = (out_line[index_s + 1:index_f])

            out_line = out_line[:index_s + 1] + "DIR" + out_line[index_f:]



        while (out_line.endswith(" ")):
            out_line = out_line[:-1]

        # print "PC:",str(pc)+" -",out_line
        if out_line.__contains__(','):
            char = out_line[out_line.index(',') + 1]
            # print char
            if (char.isdigit()):
                # print char
                if out_line[out_line.index(',') + 1:].isdigit():
                    content = out_line[out_line.index(',') + 1:]
                    out_line = out_line[: out_line.index(",") + 1] + "LIT"
            elif (char == "#"):
                # print (out_line[out_line.index(',') + 2:])

                try:
                    int_val = str(int((out_line[out_line.index(',') + 2:]),16))
                    content = int_val
                except:
                    content = 0


                # content = str(int((out_line[out_line.index(',') + 2:]),16))
                out_line = out_line[: out_line.index(",") + 1] + "LIT"



        # print "PC:", str(pc) + " -", out_line

        if(out_line.startswith("J")):
            out_line_split = out_line.split(" ")
            # print out_line_split
            out_line = out_line_split[0] + " DIR"
            content = out_line_split[1]

        # print line.strip()
        # print out_line+": Content = "+str(content)+"\n"


        if(load_data):
            var_name = out_line.split(" ")[0]
            var_value = out_line.split(" ")[1]
            data_dict[var_name]=[memory_data_index,var_value]
            memory_data_index+=1
        else:
            program_list.append((out_line,str(content),pc))
        # print out_line

        pc+=1

    file.close()

    return program_list,label_list,data_dict

def sort_data(data_dict):

    def get_key(item):
        return item[0]

    temp_list = []
    for data in data_dict:
        temp_list.append(data_dict[data])

    sorted_list = sorted(temp_list, key=get_key)
    return sorted_list
