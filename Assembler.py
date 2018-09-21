from utilities import *

def PrintError(string):
    print string + ",ERROR"

file = open("opcode.txt", "r")
codes = list()


for line in file:
    codes.append(tuple(list(line.strip().split('-'))))

fileName= raw_input("Ingrese el nombre del archivo: ")
#fileName = "program1.txt"
file = open(fileName)
program = list()
labels = list()

for line in file:
    program.append(line.strip().replace("\t", ""))
file.close()
# Mete los labels a una lista y los asocia con el numero de linea en el que estan


for line in program:
    ind=program.index(line)
    lineWithLabel = line.split(':')
    if len(lineWithLabel) > 1:
        labels.append((lineWithLabel[0], ind))
    program[ind] = lineWithLabel[-1]


#Reemplazo lo que esta dentro del parentesis por un DIR


list_out = []
list_content = []


for t_line in program:
    content = 0
    line = t_line

    ind = program.index(line)
    if "(" in line and ")" in line and "(A)" not in line and "(B)" not in line:
        index_s = line.index("(")
        index_f = line.index(")")

        content = line[index_s+1:index_f]
        line = line[:index_s+1]+"DIR"+line[index_f:]



    if line.find(',') != -1:
        if line[line.index(",")+1:].isdigit():
            line = line[: line.index(",")+1] + "LIT"
            program[ind] = line

    if line[0] == 'J' and line.find(',')==-1:
        line = line.split(" ")
        flag=True
        for label, indexLabel in labels:
            if line[1]==label:
                content = indexLabel
                flag=False
        if flag:
            PrintError("LABEL NOT ENCOUNTERED")
        else:
            line[1] = "DIR"
        s = " "
        s = s.join(line)
        program[ind]=s
        line = s

    list_content.append(content)
    list_out.append(line)

print codes
print list_out


flag = True
archivo = open(fileName.replace(".txt", ".out"), "w")
cont=0

for index in range(len(list_out)):
    flag=True
    for ins, opcode in codes:
        if ins == list_out[index]:
            flag = False
            archivo.write( '{0:07b}'.format(int(list_content[index])) +"_"+str(opcode)+ "\n")
            cont+=1
    if flag:
        PrintError("INSTRUCTION '"+list_out[index]+"' DOES NOT EXISTS")
if cont!=len(program):
    PrintError("ARCHIVO ASEMBLY NO VALIDO")
archivo.close()

