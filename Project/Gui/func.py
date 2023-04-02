# 必要函数

def read_file(path):
    """
    :param path:
    :return:
    """
    with open(path, 'r', encoding='utf-8') as fp:
        content = fp.read()
    return content


def save_file(content, des_path, filename):
    """

    :param path:
    :return:
    """
    des = des_path+'/'+filename+'.reg'
    with open(des, 'w', encoding='utf-8') as fp:
        fp.write(content)
