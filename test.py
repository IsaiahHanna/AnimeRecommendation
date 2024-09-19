string1 = 'qwe'
string2 = 'awd'

def string_map(s1,s2):
    for x in s1:
        if x in s2:
            return False
    return True



print(string_map(string1, string2) == True)