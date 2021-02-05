# -*- coding: utf-8 -*-
import os

'''
统计一个文件的有效代码行数
'''


def count_lines(file_name):
    if not file_name.endswith(".py"):
        return 0
    with open(file_name, encoding='utf-8') as fp:
        line_count = 0
        for line in fp.readlines():
            if not line.split():  # 判断是否为空行
                line.strip()  # 去除空行
                continue
            else:
                line_count += 1
        fp.close()
        return line_count

def mulu_statics(file_dir):
    s = 0
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file == "lines_calc.py":
                continue
            file_name = root + "\\" + file
            lines = count_lines(file_name)
            s += lines
    return s


if __name__ == '__main__':
    res = mulu_statics("./")
    print(res)
