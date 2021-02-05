import inspect
import os
import sys

from app.fota.fota_tester import FotaTester


def get_totest_classes(root="app"):
    '''
    动态加载app目录下的测试用例
    :param root: 指定的目录
    :return: 待测试的用例
    '''
    to_test_classes_dict = {}
    for root, dirs, files in os.walk(root):
        for file in files:
            if "pycache" in str(file) or str(file).endswith("pyc"):
                continue
            if "__init__" in str(file):
                continue
            # 获取文件所属目录
            # 获取文件路径
            module_name = os.path.join(root, file).replace("\\", ".").strip(".py")
            module_name = module_name[module_name.index("app"):]  # 以app为首，用作包的引入
            __import__(module_name, globals(), locals(), [], 0)
            module = sys.modules[module_name]
            module_attrs = dir(module)
            for name in module_attrs:
                var_obj = getattr(module, name)
                if inspect.isclass(var_obj):
                    if issubclass(var_obj, FotaTester) and var_obj.__name__ != FotaTester.__name__:
                        key = module_name + "." + str(var_obj.__name__)
                        desc_info = getattr(var_obj, "__func_desc__") if hasattr(var_obj, "__func_desc__") else "没有描述信息"
                        to_test_classes_dict[key] = {
                            "desc_info": desc_info,
                            "class_item": var_obj
                        }
    return to_test_classes_dict
