import sys
from Error import *
from processing import *

Vars = {                                                        #변수 저장 공간

}

def repeat(line, j, inst_line, i, token):               #반복문
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
                        rangeerror(i)
                
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
                        rangeerror(i)

                else:
                    typeerror(i, ('MULTI', 'COLON'))

            

            elif line[j+2][0] == 'USEVAR':
                    if (line[j+2][1].count("'")) in Vars.keys():
                        if Vars[line[j+2][1].count("'")] > 0:
                            for p in range(Vars[line[j+2][1].count("'")] + (line[j+2][1].count('.') - line[j+2][1].count(','))):

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
                            rangeerror(i)

                    else:
                        name(i)

            else:
                typeerror(i, ('INT', 'USEVAR'))
        else:
            syntax(i, ':')
    else:
        syntax(i, ';')

def condition(line, j, inst_line, i, token):            #조건문
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
                if (line[j+2][1].count("'")) in Vars.keys():
                    if (int(Vars[line[j+2][1].count("'")])  + line[j+2][1].count('.') - line[j+2][1].count(',')) == 0:
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
                    name(i)


            else:
                typeerror(i, ('INT', 'USEVAR'))
                
        else:
            syntax(i, ':')

    else:
        syntax(i, ';')

def makevar(line, j, token, i, inst_line):              #변수생성
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
                    typeerror(i, 'INT')

            elif line[j+3][0] == 'MULTI':
                if line[j+2][0] == 'INT' and line[j+4][0] == 'INT':
                    inst_line += 'Vars['
                    inst_line += str(token[1].count("`"))
                    inst_line += '] = '
                    inst_line += str((line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(',')))
                    exec(inst_line)

                else:
                    typeerror(i, 'INT')

            else:
                typeerror(i, ('MULTI', 'LINEEND'))

        elif line[j+2][0] == 'LINEEND':
            inst_line += 'Vars['
            inst_line += str(token[1].count("`"))
            inst_line += '] = 0'
            exec(inst_line)

        else:
            typeerror(i, ('INT', 'LINEEND'))

    else:
        syntax(i, ':')

def monoinput(line, j, i, inst_line):                   #입력
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'MAKEVAR':
            inst_line += 'Vars['
            inst_line += str(line[j+2][1].count("`"))
            inst_line += '] = '
            a = input()
            if a.isdigit():
                inst_line += a
            else:
                typeerror(i, 'INT')
            exec(inst_line)
        
        else:
            typeerror(i, 'USEVAR') 
    else:
        syntax(i, ';')

def intprint(line, j, i):                               #정수출력
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'INT':
            print(line[j+2][1].count('.') - line[j+2][1].count(','))

        elif line[j+2][0] == 'USEVAR':
            if (line[j+2][1].count("'")) in Vars.keys():
                print(Vars[line[j+2][1].count("'")]+line[j+2][1].count('.')-line[j+2][1].count(','))

            else:
                name(i)


        else:
            typeerror(i, ('INT', 'USEVAR'))
                    
    else:
        syntax(i, ';')

def strprint(line, j, i):                               #문자열출력
    if line[j+1][0] == 'SEMICOLON':
        if line[j+2][0] == 'INT':
            if line[j+3][0] == 'MULTI':
                if line[j+4][0] == 'INT':
                    if (line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(',')) > 31:
                        print(chr((line[j+2][1].count('.') - line[j+2][1].count(',')) * (line[j+4][1].count('.') - line[j+4][1].count(','))))
                    else:
                        numerror(i)
                else:
                    typeerror(i, 'INT')
            
            elif line[j+3][0] == 'LINEEND':
                if (line[j+2][1].count('.') - line[j+2][1].count(',')) > 31:
                    print(chr(line[j+2][1].count('.') - line[j+2][1].count(',')))
                else:
                    numerror(i)
            
            else:
                typeerror(i, ('INT', 'LINEEND'))
        
        elif line[j+2][0] == 'USEVAR':
                if (line[j+2][1].count("'")) in Vars.keys():
                    if int(Vars[line[j+2][1].count("'")]) > 31:
                        print(chr(int(Vars[line[j+2][1].count("'")]) + line[j+2][1].count('.') - line[j+2][0].count(',')))
                    else:
                        numerror(i)

        
        elif line[j+2][0] == 'LINEEND':
            print("\n", end = '')

    else:
        syntax(i, ';')
