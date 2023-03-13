
cPath = '../Lib1_Words_Recognize/Category'


def rCategory():
    c_dict = {}
    with open(cPath, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            div = line.split(' ')
            c_dict[div[0]] = div[1].strip()
    return c_dict

