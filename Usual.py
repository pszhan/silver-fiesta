# 定义一个字典，将颜色名称映射到对应的数字
RGBDIR = {'R': 1, 'G': 2, 'B': 3}

# 定义一个元组，包含颜色名称的顺序
RGBT = ('R', 'G', 'B')

# 定义一个字典，将数字映射到对应的颜色顺序字符串
TypetoRGB = {
    '5': "RGB",
    '6': "RBG",
    '3': "GBR",
    '4': "GRB",
    '1': "BGR",
    '2': "BRG"
}

# 定义一个字典，将RGB颜色模式映射到对应的类型代码
RGBtoType = {
    "RGB": '5',
    "NGB": '5',
    "RNB": '5',
    "RGN": '5',

    "RBG": '6',
    "NBG": '6',
    "RNG": '6',
    "RBN": '6',

    "GBR": '3',
    "NBR": '3',
    "GNR": '3',
    "GBN": '3',

    "GRB": '4',
    "NRB": '4',
    "GNB": '4',
    "GRN": '4',

    "BGR": '1',
    "NGR": '1',
    "BNR": '1',
    "BGN": '1',

    "BRG": '2',
    "NRG": '2',
    "BNG": '2',
    "BRN": '2'
}

# 定义一个字典，将三个数字的顺序映射到对应的字母
dir02 = {
    "123": 'a',
    "132": 'b',
    "213": 'c',
    "231": 'd',
    "312": 'e',
    "321": 'f'
}

# 定义一个函数，将整数元组转换为对应的类型
def IntToType(tNum=(0,0,0)):
    # 将元组中的整数转换为字符串并拼接
    s = str(tNum[0]) + str(tNum[1]) + str(tNum[2])
    # 返回字典dir02中对应键的值
    return dir02[s]

# 定义一个函数，根据输入的整数元组计算类型
def Type04(tNum):
    # 将元组中的整数减1后转换为对应的RGBT字符，并拼接
    s = RGBT[tNum[0]-1] + RGBT[tNum[1]-1] + RGBT[tNum[2]-1]
    # 返回字典RGBtoType中对应键的值
    return RGBtoType[s]

# 定义一个函数，根据任务ID和三色字符串计算类型
def Type_Task05(taskid:str, three_color:str):
    res_str = ""
    # 遍历任务ID中的每个字符
    for ic in taskid:
        # 在三色字符串中找到对应的颜色索引，加1后转换为字符串并拼接
        res_str += str(three_color.find(RGBT[ic-1])+1)
    # 返回字典dir02中对应键的值
    return dir02[res_str]

# 定义一个函数，根据输入的字符串获取对应的类型
def GetReturnType(s):
    res = 'g'
    try:
        # 尝试从字典RGBtoType中获取对应键的值
        res = RGBtoType[s]
    except:
        # 如果发生异常，将结果设置为默认值'g'
        res = 'g'
    return res



