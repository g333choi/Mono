import sys


def lexer(contents):
    lines = contents.split('\n')
    nline = []

    for line in lines:
        chars = list(line)
        temp_str = ""
        tokens = []
        for char in chars:                                      #입력 쪼개기
            if char == ":" or char == ';':                      #구분자
                tokens.append(temp_str)
                tokens.append(char)
                temp_str = ""

            elif char == '"':                                   #문장 끝
                tokens.append(temp_str)
                tokens.append(char)
                temp_str = ""

            elif char == ' ':                                   #곱셈
                tokens.append(temp_str)
                tokens.append(char)
                temp_str = ''

            elif char == '.' or char == ',' or char == '·' or char == '`' or char == "'":
                temp_str += char                                

            else:                                               #다른 문자 있을 경우 에러
                print("Error: Unknown syntax")
                sys.exit()
        
        for i in tokens:
            if '' in tokens:
                tokens.remove('')                               #'' 있을 경우 제거

        items = []
        for token in tokens:                                    #타입 판단
            IsUsevar = True
            IsMakevar = True
            IsInt = True

            if '`' in token:                                    #변수 생성 판단
                for q in token:
                    if q != '`':
                        IsMakevar = False
                if IsMakevar:
                    items.append(("MAKEVAR", token))

            elif "'" in token:
                for o in token:
                    if o != "'":
                        IsUsevar = False
                if IsUsevar:
                    items.append(("USEVAR", token))                 #변수 생성

            elif "." in token or ',' in token:                  #정수
                for h in token:
                    if h == '.' or h ==',':
                        continue
                    else:
                        IsInt = False
                if IsInt:
                    items.append(("INT", token))

            elif token == ' ':                                  #곱셈
                items.append(("MULTI", token))

            elif token == "·":                         #입력
                items.append(("INPUT", token))

            elif token == '··':                         #정수 출력
                items.append(("INTPRINT", token))

            elif token == '···':                         #문자열 출력
                items.append(("STRPRINT", token))

            elif token == '····':                         #조건문
                items.append(("CONDITION", token))

            elif token == '·····':                         #반복문
                items.append(("REPEAT", token))

            elif token == ':':                                  #콜론 구분
                items.append(("COLON", token))

            elif token == ';':                                  #세미콜론 구분
                items.append(("SEMICOLON", token))

            elif token == '"':                                  #문장 끝
                items.append(("LINEEND", token))

            else:
                print("ERROR: Unknown syntax")
                sys.exit()

        nline.append(items)
    return(nline)

Vars = {                                                        #변수 저장 공간

}


def parse(file):
    contents = open(file, 'r', encoding='UTF-8').read()
    lines = lexer(contents)

    for i in range(len(lines)):
        line = lines[i]
        inst_line = ''
        InCondition = False
        InRepeat = False

        if line[-1][0] == 'LINEEND':
            for j in range(len(line)):
                token = line[j]
                
                if token[0] == 'MAKEVAR' and line[j+1][0] != 'LINEEND' and InCondition == False and InRepeat == False:
                    makevar(line, j, token, i, inst_line)

                elif token[0] == 'INPUT' and InCondition == False and InRepeat == False:
                    monoinput(line, j, i, inst_line)
                
                elif token[0] == 'INTPRINT' and InCondition == False and InRepeat == False:
                    intprint(line, j, i)

                elif token[0] == 'STRPRINT' and InCondition == False and InRepeat == False:
                    strprint(line, j, i)
                
                elif token[0] == 'CONDITION' and InCondition == False and InRepeat == False:
                    InCondition = True
                    condition(line, j, inst_line, i, token)

                elif token[0] == 'REPEAT' and InCondition == False and InRepeat == False:
                    InRepeat = True
                    repeat(line, j, inst_line, i, token)

                elif line[0][0] == 'LINEEND' or line[0][0] == 'COLON' or line[0][0] == 'SEMICOLON' or line[0][0] == 'MULTI':
                    print("ERROR at line[{}]: Wrong type. 'INPUT', 'MAKEVAR', 'INTPRINT', 'STRPRINT', 'CONDITION' or 'REPEAT' type expected.".format(i+1))
                    sys.exit()


        else:
            print("ERROR at line[{}]: '\"' expected at the end".format(i+1))
            sys.exit()


def repeat(line, j, inst_line, i, token):
    if line [j+1][0] == 'SEMICOLON':
        if line[j+3][0] == 'COLON':
            if line[j+2][0] == 'INT':
                if line[j+3][0] == 'MULTI':
                    if ((line[j+2][1].count('.')-line[j+2][1].count(',')) * (line[j+4][1].count('.')-line[j+4][1].count(','))) > 0:
                        for p in range(line[j+2][1].count('.')-line[j+2][1].count(',')):

                            if line[j+4][0] == 'MAKEVAR':
                                makevar(line, j+4, token, i, inst_line)

                            elif line[j+4][0] == 'INPUT':
                                monoinput(line, j+4, i, inst_line)
                            
                            elif line[j+4][0] == 'INTPRINT':
                                intprint(line, j+4, i)

                            elif line[j+4][0] == 'STRPRINT':
                                strprint(line, j+4, i)
                            
                            elif line[j+4][0] == 'CONDITION':
                                condition(line, j+4, inst_line, i, token)

                            elif line[j+4][0] == 'REPEAT':
                                repeat(line, j+4, inst_line, i, token)

                    else:
                        print("ERROR at line[{}]: Wrong range. number of times must be over 0".format(i+1))
                        sys.exit()
                
                elif line[j+3][0] == 'COLON':
                    if line[j+2][1].count('.')-line[j+2][1].count(',') > 0:
                        for p in range(line[j+2][1].count('.')-line[j+2][1].count(',')):

                            if line[j+4][0] == 'MAKEVAR':
                                makevar(line, j+4, token, i, inst_line)

                            elif line[j+4][0] == 'INPUT':
                                monoinput(line, j+4, i, inst_line)
                            
                            elif line[j+4][0] == 'INTPRINT':
                                intprint(line, j+4, i)

                            elif line[j+4][0] == 'STRPRINT':
                                strprint(line, j+4, i)
                            
                            elif line[j+4][0] == 'CONDITION':
                                condition(line, j+4, inst_line, i, token)

                            elif line[j+4][0] == 'REPEAT':
                                repeat(line, j+4, inst_line, i, token)
                    
                    else:
                        print("ERROR at line[{}]: Wrong range. number of times must be over 0".format(i+1))
                        sys.exit()

                else:
                    print("ERROR at line[{}]: Wrong type. 'MULTI' or 'COLON' type expected".format(i+1))

            

            elif line[j+2][0] == 'USEVAR':
                if line[j+3][0] == 'INT':
                    if (line[j+2][1].count("'")) in Vars.keys():
                        if Vars[line[j+2][1].count("'")] > 0:
                            for p in range(Vars[line[j+2][1].count("'")] + (line[j+3][1].count('.') , line[j+3][1].count(','))):

                                if line[j+4][0] == 'MAKEVAR':
                                    makevar(line, j+4, token, i,inst_line)

                                elif line[j+4][0] == 'INPUT':
                                    monoinput(line, j+4, i, inst_line)
                                
                                elif line[j+4][0] == 'INTPRINT':
                                    intprint(line, j+4, i)

                                elif line[j+4][0] == 'STRPRINT':
                                    strprint(line, j+4, i)
                                
                                elif line[j+4][0] == 'CONDITION':
                                    condition(line, j+4, inst_line, i, token)

                                elif line[j+4][0] == 'REPEAT':
                                    repeat(line, j+4, inst_line, i, token)
                        
                        else:
                            print("ERROR at line[{}]: Wrong range. number of times must be over 0".format(i+1))
                            sys.exit()

                    else:
                        print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
                        sys.exit()

                elif line[j+3][0] == 'COLON':
                    if (line[j+2][1].count("'")) in Vars.keys():
                        if Vars[line[j+2][1].count("'")] > 0:
                            for p in range(Vars[line[j+2][1].count("'")]):

                                if line[j+4][0] == 'MAKEVAR':
                                    makevar(line, j+4, token, i,inst_line)

                                elif line[j+4][0] == 'INPUT':
                                    monoinput(line, j+4, i, inst_line)
                                
                                elif line[j+4][0] == 'INTPRINT':
                                    intprint(line, j+4, i)

                                elif line[j+4][0] == 'STRPRINT':
                                    strprint(line, j+4, i)
                                
                                elif line[j+4][0] == 'CONDITION':
                                    condition(line, j+4, inst_line, i, token)

                                elif line[j+4][0] == 'REPEAT':
                                    repeat(line, j+4, inst_line, i, token)
                        
                        else:
                            print("ERROR at line[{}]: Wrong range. number of times must be over 0".format(i+1))
                            sys.exit()

                    else:
                        print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
                        sys.exit()
                
                else:
                    print("ERROR at line[{}]: Wrong type. 'INT' or 'COLON' type expected".format(i+1))
                    sys.exit()


            else:
                print("ERROR at line[{}]: Wrong type. 'INT' or 'USEVAR' type expected".format(i+1))
                sys.exit()
        else:
            print("ERROR at line[{}]: Wrong syntax. ':' expected".format(i+1))
            sys.exit()
    else:
        print("ERROR at line[{}]: Wrong syntax. ';' expected".format(i+1))
        sys.exit()

def condition(line, j, inst_line, i, token):
    if line[j+1][0] == 'SEMICOLON':
        if line[j+3][0] == 'COLON':
            if line[j+2][0] == 'INT':
                if (line[j+2][1].count('.')-line[j+2][1].count(',')) == 0:

                    if line[j+4][0] == 'MAKEVAR':
                        makevar(line, j+4, token, i, inst_line)

                    elif line[j+4][0] == 'INPUT':
                        monoinput(line, j+4, i, inst_line)

                    elif line[j+4][0] == 'INTPRINT':
                        intprint(line, j+4, i)

                    elif line[j+4][0] == 'STRPRINT':
                        strprint(line, j+4, i)

                    elif line[j+4][0] == 'REPEAT':
                        repeat(line, j+4, inst_line, i, token)
                    elif line[j+4][0] == 'CONDITION':
                        condition(line, j+4, inst_line, i, token)
                else:
                    pass

            elif line[j+2][0] == 'USEVAR':
                if line[j+3][0] == 'INT':
                    if (line[j+2][1].count("'")) in Vars.keys():
                        if int(Vars[line[j+2][1].count("'")]) == 0:
                            if line[j+4][0] == 'MAKEVAR':
                                makevar(line, j+4, token, i, inst_line)

                            elif line[j+4][0] == 'INPUT':
                                monoinput(line, j+4, i, inst_line)

                            elif line[j+4][0] == 'INTPRINT':
                                intprint(line, j+4, i)

                            elif line[j+4][0] == 'STRPRINT':
                                strprint(line, j+4, i)

                            elif line[j+4][0] == 'REPEAT':
                                repeat(line, j+4, inst_line, i, token)
                            elif line[j+4][0] == 'CONDITION':
                                condition(line, j+4, inst_line, i, token)
                        else:
                            pass
                    else:
                        print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
                        sys.exit()

                elif line[j+3][0] == 'COLON':
                    if (line[j+2][1].count("'")) in Vars.keys():
                        if int(Vars[line[j+2][1].count("'")]) == 0:
                            if line[j+4][0] == 'MAKEVAR':
                                makevar(line, j+4, token, i, inst_line)

                            elif line[j+4][0] == 'INPUT':
                                monoinput(line, j+4, i, inst_line)

                            elif line[j+4][0] == 'INTPRINT':
                                intprint(line, j+4, i)

                            elif line[j+4][0] == 'STRPRINT':
                                strprint(line, j+4, i)

                            elif line[j+4][0] == 'REPEAT':
                                repeat(line, j+4, inst_line, i, token)
                            elif line[j+4][0] == 'CONDITION':
                                condition(line, j+4, inst_line, i, token)
                        else:
                            pass
                    else:
                        print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
                        sys.exit()

            else:
                print("ERROR at line[{}]: Wrong type. 'INT' or 'USEVAR' type expected".format(i+1))
                sys.exit()
                
        else:
            print("ERROR at line[{}]: Wrong syntax. ':' expected".format(i+1))
            sys.exit()

    else:
        print("ERROR at line[{}]: Wrong syntax. ';' expected".format(i+1))
        sys.exit()

def makevar(line, j, token, i, inst_line):
    if line[j+1][0] == 'COLON':
        if line[j+2][0] == 'INT':
            if line[j+3][0] == 'LINEEND':
                if line[j+2][0] == 'INT':
                    inst_line += 'Vars['
                    inst_line += str(token[1].count("`"))
                    inst_line += '] = '
                    inst_line += str(line[j+2][1].count('.') - line[j+2][1].count(','))
                    exec(inst_line)

                else:
                    print("ERROR at line[{}]: Wrong type. 'INT' type expected".format(i+1))
                    sys.exit()

            elif line[j+3][0] == 'MULTI':
                if line[j+2][0] == 'INT' and line[j+4][0] == 'INT':
                    inst_line += 'Vars['
                    inst_line += str(token[1].count("`"))
                    inst_line += '] = '
                    inst_line += str((line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(',')))
                    exec(inst_line)

                else:
                    print("ERROR at line[{}]: Wrong type. 'INT' type expected".format(i+1))
                    sys.exit()

            else:
                print("ERROR at line[{}]: Wrong type. 'MULTI' or 'LINEEND' type expected", format(i+1))
                sys.exit()

        elif line[j+2][0] == 'LINEEND':
            inst_line += 'Vars['
            inst_line += str(token[1].count("`"))
            inst_line += '] = 0'
            exec(inst_line)

        else:
            print("ERROR at line[{}]: Wrong type. 'INT' or 'LINEEND' type expected", format(i+1))
            sys.exit()

    else:
        print("ERROR at line[{}]: Wrong syntax. ':' expected".format(i+1))
        sys.exit()

def monoinput(line, j, i, inst_line):
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'MAKEVAR':
            inst_line += 'Vars['
            inst_line += str(line[j+2][1].count("`"))
            inst_line += '] = '
            a = input()
            if a.isdigit():
                inst_line += a
            else:
                print("ERROR at line[{}]: Wrong type. 'INT' type needs to be entered".format(i+1))
                sys.exit()
            exec(inst_line)
        
        else:
            print("ERROR at line[{}]: Wrong type. 'USEVAR type expected".format(i+1))
            sys.exit()   
    else:
        print("ERROR at line[{}]: Wrong syntax. ';' expected".format(i+1))
        sys.exit()

def intprint(line, j, i):
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'INT':
            print(line[j+2][1].count('.') - line[j+2][1].count(','))

        elif line[j+2][0] == 'USEVAR':                              #Make Name error
            if (line[j+2][1].count("'")) in Vars.keys():
                print(Vars[line[j+2][1].count("'")])
            else:
                print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))

        else:
            print("ERROR at line[{}]: Wrong type. 'INT' or 'USEVAR' type expected".format(i+1))
            sys.exit()
                    
    else:
        print("ERROR at line[{}]: Wrong syntax. ';' expected".format(i+1))
        sys.exit()

def strprint(line, j, i):
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'INT':
            if line[j+3][0] == 'MULTI':
                if line[j+4][0] == 'INT':
                    if (line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(',')) > 31:
                        print(chr((line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(','))))
                    else:
                        print("ERROR at line[{}]: Wrong number. Number must be over 31".format(i+1))
                        sys.exit()
                else:
                    print("ERROR at line[{}]: Wrong type. 'INT' type expected".format(i+1))
                    sys.exit()
            
            elif line[j+3][0] == 'LINEEND':
                if (line[j+2][1].count('.') - line[j+2][1].count(',')) > 31:
                    print(chr(line[j+2][1].count('.') - line[j+2][1].count(',')))
                else:
                    print("ERROR at line[{}]: Wrong number. Number must be over 31".format(i+1))
                    sys.exit()
            
            else:
                print("ERROR at line[{}]: Wrong type. 'INT' or 'LINEEND' type expected".format(i+1))
                sys.exit()
        
        elif line[j+2][0] == 'USEVAR':
            if (line[j+2][1].count("'")) in Vars.keys():
                if int(Vars[line[j+2][1].count("'")]) > 31:                             #Make Name error
                    print(chr(int(Vars[line[j+2][1].count("'")])))
                else:
                    print("ERROR at line[{}]: Wrong number. Number must be over 31".format(i+1))
                    sys.exit()
            else:
                print("ERROR at line[{}]: Wrong name. Variable has to be made first".format(i+1))
        
        elif line[j+2][0] == 'LINEEND':
            print("\n", end = '')

    else:
        print("ERROR at line[{}]: Wrong syntax. ';' expected".format(i+1))
        sys.exit()
