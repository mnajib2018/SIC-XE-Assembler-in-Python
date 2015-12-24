import random, re,sys, math, string
from string import whitespace
base_Val = 0
found_BASE = False
is_NUM = False
Records = []
#program_Length = 0
OPCODETAB = {'ADD':[3,'18',1],'ADDF':[3,'58',1],'ADDR':[2,'90',2],'AND':[3,'40',1],'CLEAR':[2,'B4',1],
            'COMP':[3,'28',1],'COMPF':[3,'88',1],'COMPF':[3,'88',1],'COMPR':[2,'A0',2],'DIV':[3,'24',1],'DIVF':[3,'64',1],
            'DIVR':[2,'9C',2],'FIX':[1,'C4',0],'FLOAT':[1,'C0',0],'HIO':[1,'F4',0],'J':[3,'3C',1],
            'JEQ':[3,'30',1],'JGT':[3,'34',1],'JLT':[3,'38',1],'JSUB':[3,'48',1],'LDA':[3,'00',1],
            'LDB':[3,'68',1],'LDCH':[3,'50',1],'LDF':[3,'70',1],'LDL':[3,'08',1],'LDS':[3,'6C',1],
            'LDT':[3,'74',1],'LDX':[3,'04',1],'LPS':[3,'D0',1],'MUL':[3,'20',1],'MULF':[3,'60',1],
            'MULR':[2,'98',2],'NORM':[1,'C8',0],'OR':[3,'44',1],'RD':[3,'D8',1],'RMO':[2,'AC',2],
            'RSUB':[3,'4C',0],'SHIFTL':[2,'A4',2],'SHIFTR':[2,'A8',2],'SIO':[1,'FO',0],'SSK':[3,'EC',1],
            'STA':[3,'OC',1],'STB':[3,'78',1],'STCH':[3,'54',1],'STF':[3,'80',1],'STI':[3,'D4',1],
            'STL':[3,'14',1],'STS':[3,'7C',1],'STSW':[3,'E8',1],'STT':[3,'84',1],'STX':[3,'10',1],
            'SUB':[3,'1C',1],'SUBF':[3,'5C',1],'SUBR':[2,'94',2],'SVC':[2,'B0',1],'TD':[3,'E0',1],
            'TIO':[1,'F8',0],'TIX':[3,'2C',1],'TIXR':[2,'B8',1],'WD':[3,'DC',1]
            }

SYMTAB = {'PC':8, 'SW':9, 'A':0, 'X':1,'L': 2,'B':3, 'S':4, 'T':5, 'F':6}
REGISTERS = {'PC':8, 'SW':9, 'A':0, 'X':1,'L': 2,'B':3, 'S':4, 'T':5, 'F':6}
"""
format2a = {'ADDR':'90', 'COMPR':'A0', 'DIVR':'9C', 'MULR':'98','RMO':'AC',
            'SHIFTL':'A4', 'SHIFTR':'A8','SUBR':'94'}
format2b = {'CLEAR':'B0','SVC':'B0', 'TIXR':'B8'}
Possible Errors:
1) X byte with space
2) uppercase and lowercase Labels
3) convert hex start address-DONE
4) Add object code for BYTE and WORD
5) Add object code for #numbers - then mode is always Direct
6) PC-Location if last line-DONE

"""
def pad_displacement(digits,length):
     while len(digits) < length:
          digits = '0'+digits
     return digits

def assemble_Instruction(Lines,line_num,SYMTAB,address_Mode):
     current_line = Lines[line_num][1]
     mnemonic = current_line['mnemonic']
     OPCODE = OPCODETAB[mnemonic][1].lower()
     FORMAT = OPCODETAB[mnemonic][0]
     OP_NUM = OPCODETAB[mnemonic][2]
     NI_mode = current_line['mode']
     operand1 = current_line['operand1']
     operand2 = current_line["operand2"]
     #label_location = SYMTAB[operand1]
     extended = current_line['extended']
    

     if len(OPCODE) == 1:
          OPCODE = '0'+OPCODE
     print "HERE IS OPCODE"
     print OPCODE

     if extended == '+':
            if NI_mode == '@':
                 OPCODE = int(OPCODE,16) + 2
            elif NI_mode == '#':
                 OPCODE = int(OPCODE,16) + 1
            else:
                 OPCODE = int(OPCODE,16) + 3
            OPCODE = hex(int(OPCODE)).split('x')[1]
            if len(OPCODE) == 1:
                 OPCODE = '0'+OPCODE
            FORMAT = 4
            if OP_NUM ==  0:
                object_code = OPCODE+"100000"
                print object_code
                return object_code

            if operand1 in SYMTAB:
                 label_location = SYMTAB[operand1]
                 print "Lets do label location"
                 print label_location
                 label_location = hex(int(label_location)).split('x')[1]
                 label_location = pad_displacement(str(label_location),FORMAT + 1)
            elif NI_mode == "#" or NI_mode == '@':
                 if operand1.isdigit():
                      print "IT's A DIGIT"
                      label_location = hex(int(operand1)).split('x')[1]
                      label_location = pad_displacement(str(label_location),FORMAT + 1)
                      
            else:
                 label_location = 0
                 label_location = pad_displacement(str(label_location),FORMAT + 1)
             
            if operand2:
                 if operand2[0] == 'X' or operand2[0] == 'x':
                    xbpi_byte = 9
            else:
                    xbpi_byte = 1
           
            xbpi_byte = hex(xbpi_byte).split('x')[1]       
            target_address = xbpi_byte+label_location
            print target_address
            object_code = OPCODE +target_address
            print object_code
            return object_code

     elif FORMAT == 3: 
            if NI_mode == '@':
                 OPCODE = int(OPCODE,16) + 2
            elif NI_mode == '#':
                 OPCODE = int(OPCODE,16) + 1
            else:
                 OPCODE = int(OPCODE,16) + 3
            OPCODE = hex(int(OPCODE)).split('x')[1]
            if len(OPCODE) == 1:
                 OPCODE = '0'+OPCODE
            if OP_NUM ==  0:
                  object_code = OPCODE+"0000"
                  print object_code
                  return object_code

            print mnemonic
            print operand1
            #if operand1 in SYMTAB PROBLEM HERE
            #label_location = SYMTAB[operand1]
            if operand1 in SYMTAB:
                 intlabel_location = SYMTAB[operand1]
                 print "Let's do label location"
                 print intlabel_location
                 label_location = hex(int(intlabel_location)).split('x')[1]
                 
            elif NI_mode == "#" or NI_mode == '@':
                 if operand1.isdigit():
                      print "IT's A DIGIT"
                      intlabel_location = int(operand1)
                      if int(operand1) > 4095:
                           print "operand value too large for format 3"
                           sys.exit()
                      label_location = hex(int(operand1)).split('x')[1]
                      address_Mode = 'Direct'
            else:
                 intlabel_location = 0
                 label_location = 0
                 
            xbpi_byte = 0

            if(address_Mode == 'Direct'):
               if operand2:
                      if operand2[0] == 'X' or operand2[0] == 'x':
                           xbpi_byte = 8
                      else:
                           xbpi_byte = 0
               print "HERE IS label location"
               print label_location
               
               #label_location = hex(int(label_location)).split('x')[1]  
               #print label_location
               label_location = pad_displacement(label_location,FORMAT)
               xbpi_byte = hex(xbpi_byte).split('x')[1]       
               target_address = xbpi_byte+label_location
               print target_address
               object_code = OPCODE +target_address
               print object_code
               return object_code

            elif(address_Mode == 'PC'):
               if operand2:
                      if operand2[0] == 'X' or operand2[0] == 'x':
                           xbpi_byte = 10
                      else:
                           xbpi_byte = 2
               else:
                    xbpi_byte = 2
               xbpi_byte = hex(xbpi_byte).split('x')[1]  
               print "XBPI"
               print xbpi_byte
               PC_location = Lines[line_num+1][0]
               if PC_location == '':
                    print "Alternate PC"
                    PC_location = Lines[line_num][0]
               displacement =  intlabel_location-int(PC_location)
               
               if displacement >= 0:
                    displacement = hex(int(displacement)).split('x')[1]
               else:
                    print "NEGATIVE"
                    print displacement
                    displacement = hex(0xfff & int(displacement)).split('x')[1]
               displacement = pad_displacement(displacement,FORMAT)     
               print displacement
               target_address = xbpi_byte + displacement
               object_code = OPCODE + target_address
               print object_code.lower()
               print OP_NUM
               return object_code

            elif(address_Mode == 'BASE'):
               if operand2:
                      if operand2[0] == 'X' or operand2[0] == 'x':
                           xbpi_byte = 12
                      else:
                           xbpi_byte = 4
               else:
                    xbpi_byte = 4
               xbpi_byte = hex(xbpi_byte).split('x')[1]       
               
               base_location = base_Val
               displacement = intlabel_location - int(base_location)
               displacement = hex(int(displacement)).split('x')[1]
               displacement = pad_displacement(displacement,FORMAT)
               target_address = xbpi_byte + displacement
               object_code = OPCODE + target_address
               print object_code
               return object_code

     if FORMAT == 2:
          if OP_NUM == 2:
               print "mnemonic"
               print mnemonic
               if mnemonic.upper() == 'SHIFTR'or mnemonic.upper() == "SHIFTL":
                 r1 = SYMTAB[operand1]
                 if operand2 in SYMTAB or operand2 in REGISTERS:
                      print mnemonic + "takes a second operand between 1 and 16"
                      sys.exit()
                 if operand2 > 16 or operand < 1 :
                      print mnemonic + "needs an operand2 between 1 and 16"
                 n = operand2
                 n = int(n)-1
                 n = hex(int(n)).split('x')[1]
                 r2 = n
               else:
                    r1 = SYMTAB[operand1]
                    r2 = SYMTAB[operand2]
  
               print OPCODE
               object_code = OPCODE + str(r1) + str(r2)
               print object_code
               return object_code

          elif OP_NUM == 1:
               if mnemonic.upper() == 'TIXR'or mnemonic.upper() == "CLEAR":
                    if not operand1 in REGISTERS:
                         print "REGISTER NOT RECOGNIZED"
                         sys.exit()
                    r1 = REGISTERS[operand1]
                    r2 = 0
                    object_code = OPCODE + str(r1)+str(r2)
                    print object_code
                    return object_code
               if mnemonic.upper() == 'SVC':
                    r1 =hex(int(operand1)).split('x')[1]
                    r2 = 0
                    object_code = OPCODE + str(r1)+str(r2)
                    print object_code
                    return object_code
                    
     if FORMAT == 1:
          object_code = OPCODE
          print OPCODE
          return object_code





def find_Mode(Lines,line_num,SYMTAB):
     current_line = Lines[line_num][1]
     current_location = Lines[line_num][0]
     PC_location = Lines[line_num+1][0]
     if PC_location == '':
          print "Alternate PC"
          PC_location = Lines[line_num][0]
     mnemonic = current_line['mnemonic']
     OPCODE = OPCODETAB[mnemonic][1].lower()
     FORMAT = OPCODETAB[mnemonic][0]
     OP_NUM = OPCODETAB[mnemonic][2]
     NI_mode = current_line['mode']
     operand1 = current_line['operand1']
     operand2 = current_line["operand2"]
     #label_location = SYMTAB[operand1]
     extended = current_line['extended']
     print str(PC_location)
     print "PCLOCAATION"
     print operand1
   
     if operand1 in SYMTAB:
                 label_location = SYMTAB[operand1]
                 print "Lets do label location"
                 print label_location
                 
     elif NI_mode == "#"or NI_mode == '@':
                 if operand1.isdigit():
                      print "IT's A DIGIT"
                      return 'Direct'
                      
     else:
                 label_location = 0
                

     
     if extended == "+":
          return 'extended'
     


     if FORMAT == 3:
          if label_location < 4096:
               return 'Direct'
          elif int(PC_location) - int(label_location) < 2048 and int(PC_location) - int(label_location) > -2049:
               return 'PC'
          elif found_BASE == True:
               if location - base_Val < 4096 and location - base_Val > 0 :
                    return 'BASE'
               else:
                    return 'SIC'   
          else:
               return 'SIC'   
     elif FORMAT == 2:
          return 'Mode2'
     elif FORMAT == 1:
          return 'Mode1'

def pad_Name(name):
     print "name before: "+name
     if len(name) < 6:
          for i in range(len(name),6):
               name = name + " "
     print "name after:  "+name+"78899"
     print "name after:  "+"123456"
     return name

def padstart_Address(name):
     if len(str(name)) < 6:
          for i in range(len(str(name)),6):
               name = "0"+str(name)
     return name 

def labelRE(line):
     RE = r'(?P<label>[A-Za-z]?\w*)\s*(?P<extended>[+]?)\s*(?P<mnemonic>[A-Za-z]*)\s*(?P<mode>[#@]*)\s*(?P<operand1>[A-Za-z]*[0-9]*)\s*[,\']*\s*(?P<operand2>\w*)'
     match = re.match(RE,line)
     if match.group("operand1") == 'C' or match.group("operand1") == 'c':
          RE  = r'(?P<label>[A-Za-z]?\w*)\s*(?P<extended>[+]?)\s*(?P<mnemonic>[A-Za-z]*)\s*(?P<mode>[#@]*)\s*(?P<operand1>[A-Za-z]*[0-9]*)\s*[,\']*\s*(?P<operand2>[^\']*)'
          match = re.match(RE,line)
     if match:
         return {'label':match.group("label"),'extended':match.group("extended"),'mnemonic':match.group("mnemonic"),'mode':match.group("mode"),'operand1':match.group("operand1"),'operand2':match.group("operand2")}
     else:
         return None

def is_Comment(line):
    print line+"comment line"
    match = labelRE(line)
    if(match):
          mnemonic = match['mnemonic']
          if mnemonic == '':
              print "check1"
              return True
    elif not line:
        print "not line"
        return True
    elif len(line) == 0:
        print line
        print len(line)
        print "this above is len(line)"
        return True
    elif line == '\n':
      print "check2"  
      return True
    elif(line.lstrip() == None):
      print "check3"  
      return True
    elif(line.lstrip()[0] == '.'): 
      print "check4"  
      return True
    else:
      print "check5"  
      return False
 
def find_Length(Operand1,Operand2):
    if re.match(r'X|x',Operand1):
        print "Operand Before: " +Operand2
        print "Operand After: " + Operand2
        if re.match(r'^([A-Fa-f]|[0-9])*',Operand2):
             size = math.ceil(float(len(Operand2))/2)
             print "HERE IS SIZE  "
             print size
             return int(size)
        else:
             print "Operand 2 not valid"
             sys.exit()
    elif re.match(r'C|c',Operand1):
        print "Operand before: "+ Operand2
        print "Operand after: " + Operand2
        print Operand2
        size = math.ceil(len(Operand2))
        return int(size)


     
def to_ASCII(address):
     buffer = ''
     for i in range(0,len(str(address))-1,2):
          one_byte = address[i]+address[i+1]
          integer1 = int(one_byte,16)
          one_byte = chr(integer1) 
          buffer = buffer+one_byte
     return buffer
     





def main():
  #Open Input and Output files
  global inputfile
  global outputfile
  global outputfile2
  inputfile = open("lab8.asm", "r")
  outputfile = open("lab8.obj","w")
  outputfile2 = open("lab8out.txt","w")
  #Read first line while comment
  nextline = inputfile.readline()
 
  while(is_Comment(nextline)):
    nextline = inputfile.readline()
  
   
  mnemonic = ''
  label = ''
  operand1 = ''
  operand2 = ''
  extended = ''
  mode = ''
  match = labelRE(nextline)
  if(match):
      print match
      mnemonic = match['mnemonic']
      label = match['label']
      operand1 = match['operand1']
      operand2 = match['operand2']
      extended = match['extended']
      mode = match['mode']
  else:                       
      print "Invalid Instruction"
      sys.exit()


  start_Address = 0
  LOCCTR = 0
  Lines = []
 
 
  if mnemonic == 'START':
      start_Address = int(operand1,16)
      #start_Address = int(operand1)
      LOCCTR = start_Address
      newline = [LOCCTR,match]
      Lines.append(newline)
  
      nextline = inputfile.readline()
      while(is_Comment(nextline)):
          nextline = inputfile.readline()
          print nextline
      match = labelRE(nextline)
      if(match):
          mnemonic = match['mnemonic']
          label = match['label']
          operand1 = match['operand1']
          operand2 = match['operand2']
          extended = match['extended']
          mode = match['mode']
          if not mnemonic == 'END':
              newline = [LOCCTR,match]
              Lines.append(newline)
      else:                       
           print "Invalid Instruction"
           sys.exit()
  else:
       newline = [LOCCTR,match]
       Lines.append(newline)

  while mnemonic != 'END' :
      if label:
          if label in SYMTAB:
                  print "Error: DUPLICATE SYMBOL "+label
                  print SYMTAB
                  print label
                  sys.exit()

          else:
                  SYMTAB[label]= LOCCTR
                
      if(extended == '+'):
          if(mnemonic in OPCODETAB):
                  LOCCTR = LOCCTR + 4
      elif mnemonic in OPCODETAB:
          if(OPCODETAB[mnemonic][0] == 3):
              LOCCTR = LOCCTR + 3
          elif(OPCODETAB[mnemonic][0] == 2):
              LOCCTR = LOCCTR + 2
          elif(OPCODETAB[mnemonic][0] == 1):
              LOCCTR = LOCCTR + 1
          
      elif mnemonic.upper() == 'WORD':
              LOCCTR = LOCCTR + 3
      elif mnemonic.upper() == 'RESW':
              LOCCTR = 3*(int(operand1)) + LOCCTR
      elif mnemonic.upper() == 'RESB':
              LOCCTR = int(operand1)+LOCCTR
      elif mnemonic.upper() == 'BYTE':
          print operand2
          byte_Length = find_Length(operand1,operand2)
          print byte_Length
          print LOCCTR
          LOCCTR = byte_Length + LOCCTR
	  print LOCCTR
      else:
          print "Error: OPCODE NOT RECOGNIZED" 
          print mnemonic+"this is mnemonic"
          sys.exit()
       
      nextline = inputfile.readline()
      while(is_Comment(nextline)):
          nextline = inputfile.readline()
      match = labelRE(nextline)
      if(match):
          mnemonic = match['mnemonic']
          label = match['label']
          operand1 = match['operand1']
          operand2 = match['operand2']
          extended = match['extended']
          mode = match['mode']
          if not mnemonic.upper() == 'END' and not mnemonic.upper() == 'BASE':
              newline = [LOCCTR,match]
              Lines.append(newline)   
          elif mnemonic.upper() == 'BASE':	
              nextline = inputfile.readline()
              found_BASE = True		    
              while(is_Comment(nextline)):
                nextline = inputfile.readline()
              print mnemonic + "THIS 7 THIS"  	
              match = labelRE(nextline)
              if(match):
                    mnemonic = match['mnemonic']
                    label = match['label']
                    operand1 = match['operand1']
                    operand2 = match['operand2']
                    extended = match['extended']
                    mode = match['mode']
                    if not mnemonic.upper() == 'END'and not mnemonic.upper() == 'BASE':
                         newline = [LOCCTR,match]
                         Lines.append(newline)
      else:
      	 print "Invalid Instruction"
      	 sys.exit()	             
                     
  newline = ['',match]
  Lines.append(newline)
  global program_Length
  program_Length = LOCCTR-start_Address
  for mylist in Lines:
       print mylist
  print LOCCTR
  print SYMTAB
  print "THIS IS program Length"
  print program_Length
  # print firstline


  
  """
  ++++++++++++++++++++++++++++++++++++++++++
  +++     PASS TWO +++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  ++++++++++++++++++++++++++++++++++++++++++
  """


  if program_Length:
  #for mylist in Lines:
       line_num = 0
       nextline = Lines[line_num][1]
       LOCCTR = Lines[line_num][0]
       mnemonic = nextline['mnemonic']
       label = nextline['label']
       program_Name = ''
       if mnemonic.upper() == 'START':
            program_Name = label
            line_num += 1
            nextline = Lines[line_num][1]
            LOCCTR = Lines[line_num][0]
       program_Name = pad_Name(program_Name)
       start_Address = hex(start_Address).split('x')[1]
       start_Address = padstart_Address(start_Address)
       start_Address = to_ASCII(start_Address)
       #program_Name = to_ASCII(program_Name)
       total_Length = hex(int(program_Length)).split('x')[1]
       total_Length = padstart_Address(total_Length)
       total_Length = to_ASCII(total_Length)
       outputfile.write ('H'+program_Name+start_Address+total_Length)  #This is Listing line
       #listing_line = 'T'
       mnemonic = nextline['mnemonic']
       operand1 = nextline['operand1']
       operand2 = nextline['operand2']
       extended = nextline['extended']
       mode = nextline['mode']
     
       while not mnemonic.upper() == 'END':
            print "check11"
            if mnemonic.upper() in OPCODETAB:
                 print "check12"
                 print mnemonic
                 if operand1:
                      print "check13"
                      print nextline
                      print operand1
                      print operand2
                      print mode
                      print "mode"
                      if operand1 in SYMTAB:
                           print "check14"
                           operand_Address = SYMTAB[operand1]
                           print str(operand_Address) + "opaddress"
                      
                      elif mnemonic.upper() == 'SVC':
                           if int(operand1) > 16 or int(operand1) < 1:
                                print "Operand1 not SVC operand"
                                print operand1
                                sys.exit()
                           else:
                                print "HELLO"
                      elif mode == '#' or mode == '@':
                           print "immediate mode"
                           if (operand1.isdigit()):
                                operand_Address = int(operand1)
                      else:
                           operand_Address = 0
                           print "undefined symbol"
                           print operand1
                           sys.exit()
                 else:
                      operand_Address = 0
                      
                 if extended == '+':
                      address_Mode = 'extended'
                 else:
                      address_Mode = find_Mode(Lines,line_num,SYMTAB)  
                      
                 print "address_Mode "+ address_Mode
                 
                 my_code = assemble_Instruction(Lines,line_num,SYMTAB,address_Mode)     
                 print "MYCODE"
                 print my_code
                 out_Location = hex(int(LOCCTR)).split('x')[1]
                 outputfile2.write(str(out_Location)+" "+my_code+"\n")
                 one_Record = [LOCCTR, my_code]
                 Records.append(one_Record)

            elif mnemonic.upper() == "WORD":
                 if not operand1.isdigit():
                      print "operand for WORD should have type int"
                 num_of_bytes = int(operand1)
                 num_of_bytes = hex(num_of_bytes).split('x')[1]
                 while len(num_of_bytes) < 6:
                      num_of_bytes = '0'+ num_of_bytes
                 out_Location = hex(int(LOCCTR)).split('x')[1]
                 outputfile2.write(str(out_Location)+" "+num_of_bytes+"\n")
                 one_Record = [LOCCTR, num_of_bytes]
                 Records.append(one_Record)


            elif mnemonic.upper() == "BYTE":
                 print "It is a BYTE"
                 byte = ''
                 if operand1 == 'X' or operand1 == 'x':
                      if len(operand2) % 2 == 1:
                           operand2 = "0" + str(operand2)
                  
                      for i in range(0,len(operand2),2):
                           byte = byte + str(operand2[i]) + str(operand2[i+1])
                      out_Location = hex(int(LOCCTR)).split('x')[1]
                      outputfile2.write(str(out_Location)+" "+ byte +"\n")
                      one_Record = [LOCCTR, byte]
                      Records.append(one_Record)

                 byte = ''
                 if operand1 == 'C' or operand1 == 'c':
                      for character in operand2:
                           #byte += str(ord(str(character)))
                           byte += hex(ord(str(character))).split('x')[1]
                      out_Location = hex(int(LOCCTR)).split('x')[1]
                      outputfile2.write(str(out_Location)+" "+ byte +"\n")
                      one_Record = [LOCCTR, byte]
                      Records.append(one_Record)     
                           
            line_num += 1
            nextline = Lines[line_num][1]
            LOCCTR = Lines[line_num][0]
            mnemonic = nextline['mnemonic']
            label = nextline['label']
            operand1 = nextline['operand1']
            operand2 = nextline['operand2']
            extended = nextline['extended']
            mode = nextline['mode']

def pad_bytes(digits,length):
     while len(digits) < length:
          digits = '0'+digits
     return digits
          


def print_T_Records(Tlist):
     first_Location = (hex(int(Tlist[0]))).split('x')[1]
     first_Location = pad_bytes(first_Location,6)
     print first_Location
     first_Location = to_ASCII(first_Location)
     record_Size = (hex(int(Tlist[1]))).split('x')[1]
     record_Size = pad_bytes(record_Size,2)
     print record_Size
     record_Size = to_ASCII(record_Size)
     instructions_code = Tlist[2]
     instructions_code = to_ASCII(instructions_code)
     #print first_Location
     #print record_Size
     #print instructions_code
     print "YES"
     Text_line = 'T'+ first_Location + record_Size + instructions_code
     #Text_line =  str(hex(int(Tlist[0])).split('x')[1])+str(hex(int(Tlist[1])).split('x')[1])+str(Tlist[2])
     # print Text_line,"HERE"
     #Text_line = to_ASCII(Text_line)
     ###print'T'+ Text_line
     return Text_line



def print_Records():
     num = 0
     T_length = 0
     T_start_location = Records[num][0]
     Spaces_Left = 64
     T_Record = []
     next_location = 0
     while (num < len(Records)):
          Bytes = ''
          current_Location = Records[num][0]
          intermediate_location = current_Location      #may give error for next T 
          object_Code = Records[num][1]
          if not num+1 >= len(Records):
               next_location = Records[num+1][0]
          while (next_location - intermediate_location) <= Spaces_Left:
               if (next_location - intermediate_location) > len(object_Code):
                    num = num + 1
                    break
               Bytes = Bytes + object_Code
               Spaces_Left -= (next_location - intermediate_location)
               intermediate_location = Records[num][0]
               if(num + 1 >= len(Records)):
                    num = num + 1
                    break;
               num += 1
               object_Code = Records[num][1]
               next_location = Records[num][0]
          T_Length_2 = len(Bytes)/2
          Spaces_Left = 64
          if not num >= len(Records):
               next_location = Records[num][0]
          #T_Length = next_location - current_Location
          Text_Record = [current_Location,T_Length_2,Bytes]
          print Text_Record
          NEXT_LINE = print_T_Records(Text_Record)
          outputfile.write(NEXT_LINE)
          print NEXT_LINE
          #Text_line =  str(hex(int(Text_Record[0])).split('x')[1])+str(hex(int(Text_Record[1])).split('x')[1])+str(Text_Record[2])
          #print Text_line,"HERE"
          #Text_line = print_T_Records(Text_Record)
          #print'T'+ Text_line
          print "End of loop Here"


if __name__ == "__main__":
    main()
    #print_Records()
    print "program_Length"
    print program_Length
    print Records
    print_Records()
