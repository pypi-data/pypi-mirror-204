# -*- coding: utf-8  -*-
# -*- author: jokker -*-


import os
from JoTools.txkjRes.deteRes import DeteRes
from JoTools.utils.FileOperationUtil import FileOperationUtil

xml_dir = r"C:\Users\14271\Desktop\result_xml"
res_dir = r"C:\Users\14271\Desktop\txt_dir"

index = 0
for each_xml_path in FileOperationUtil.re_all_file(xml_dir, endswitch=[".xml"]):
    index += 1
    print(index, each_xml_path)
    dete_res = DeteRes(each_xml_path)
    each_txt_path = os.path.join(res_dir, FileOperationUtil.bang_path(each_xml_path)[1] + ".txt")
    dete_res.save_to_yolo_txt(each_txt_path)















