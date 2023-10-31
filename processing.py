import sys
import Interpreter as inter
import Error as error

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
                    inter.makevar(line, j, token, i, inst_line)

                elif token[0] == 'INPUT' and InCondition == False and InRepeat == False:
                    inter.monoinput(line, j, i, inst_line)
                
                elif token[0] == 'INTPRINT' and InCondition == False and InRepeat == False:
                    inter.intprint(line, j, i)

                elif token[0] == 'STRPRINT' and InCondition == False and InRepeat == False:
                    inter.strprint(line, j, i)
                
                elif token[0] == 'CONDITION' and InCondition == False and InRepeat == False:
                    InCondition = True
                    inter.condition(line, j, inst_line, i, token)

                elif token[0] == 'REPEAT' and InCondition == False and InRepeat == False:
                    InRepeat = True
                    inter.repeat(line, j, inst_line, i, token)

                elif line[0][0] == 'LINEEND' or line[0][0] == 'COLON' or line[0][0] == 'SEMICOLON' or line[0][0] == 'MULTI':
                    inter.typeerror(i, ('INPUT', 'MAKEVAR', 'INTPRINT', 'STRPRINT', 'CONDITION', 'REPEAT'))


        else:
            error.syntax(i, '"')

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
                    if o != "'" and o != '.' and o != ',':
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
