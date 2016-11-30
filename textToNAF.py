# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 09:55:59 2016

@author: zuoxiaolei
"""
import os
def text2NAF(content,date,title,publicId,url):
    '''
    生成规定格式的NAF文件
    '''
    if os.path.exists("nafFile"):
        pass
    else:
        os.mkdir("nafFile")

    with open("nafFile/"+title+".naf",'w') as fh:
        fh.write('<?xml version="1.0" encoding="utf-8"?>'+'\n')
        fh.write('<NAF xml:lang="en" version="v3">'+'\n')
        fh.write("<nafHeader>\n")
        fh.write("<fileDesc creationtime="+'"'+date+'"'+" title="+'"'+title+'"'+" />"+"\n")
        fh.write("<public publicId="+'"'+publicId+'"'+" uri="+'"'+url+'"'+" />"+"\n")
        fh.write("</nafHeader>"+"\n")
        fh.write("<raw><![CDATA["+content+"]]></raw>"+"\n")
        fh.write("</NAF>")

if __name__ == "__main__":
    text2NAF("123344","1234","1234","1234","1234")
        