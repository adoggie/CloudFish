# coding=utf-8
from datetime import *
import os,time
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import xml.dom.minidom
from xml.dom import minidom
import os.path
import shutil
import zipfile
import uuid


# OFD转换主函数
#filepath       字符串 原始文件路径
#DocID          字符串 UUID 文档序号
#title          字符串 发文标题
#Author         字符串 签发人
#Subject        字符串 主题词
#Abstract       字符串 摘要
#ModDate        字符串 成文日期 类似 2015-01-01
#DocUsage       字符串
#Keywords       一维数组 关键字
#CustomDatas    字典 自定义数据段 {'name': 'abc', 'title': 'xyz'}
#uploadurl      字符串 上传文件URL
#checkurl       字符串 检查上传结果URL
#savepath       字符串 保存文件路径
#返回值：转换后的文件路径，错误返回空字符串
def filetoofd(filepath,DocID, title, Author, Subject, Abstract, ModDate, DocUsage, Keywords, CustomDatas ,uploadurl ,checkurl,savepath ):
    #  参数校验
    if filepath == "" or Author=="" or Subject=="" or ModDate=="" :
        return ""
    try:
        time.strptime(ModDate, "%Y-%m-%d")
    except:
        return ""
    # 文件是否存在校验
    if not os.path.exists(filepath):
        return ""
    #生成main.xml
    xml_path = os.path.dirname(filepath)  + os.sep + "Main.xml"
    try:
        write_ofdmain_xml(xml_path, title,  os.path.basename(filepath) )
    except:
        return ""

    #生成Meta.xml
    xml_meta_path = os.path.dirname(filepath)  + os.sep + "Meta.xml"
    try:
        write_ofdmeta_xml(xml_meta_path,DocID,title, Author, Subject, Abstract, ModDate, DocUsage, Keywords, CustomDatas)
    except:
         return ""


    #生成ZIP文件
    try:
        zipname = filepath + ".zip"
        fzip = zipfile.ZipFile(zipname, 'w' ,zipfile.ZIP_DEFLATED)
        fzip.write(filepath,os.path.basename(filepath))
        fzip.write(xml_path,os.path.basename(xml_path))
        fzip.write(xml_meta_path,os.path.basename(xml_meta_path))
        fzip.close()
    except:
        return ""

    retpath =""
    #上传文件
    try:
        retpath = doctoofd(zipname,uploadurl ,checkurl)
    except:
        print "doctoofd error"
        return ""
    print "len(retpath) = " + str(len(retpath))
    if len(retpath) > 0:
        retpath = savepath + os.sep + time.strftime("%Y-%m-%d", time.localtime()) +  os.sep + retpath + ".ofd"
        if not os.path.exists(retpath):
            return ""
        else:
            print "retpath == " + retpath
            return retpath
    else:
        return ""
    return retpath


def doctoofd(filepath,uploadurl ,checkurl):
    #测试网址 http://localhost:8080/cpcns-convert-server/console/check.jsp
    #传输文件
    try:
        register_openers()
        datagen, headers = multipart_encode({"file": open(filepath, "rb")})
        request = urllib2.Request(uploadurl, datagen, headers)
        Ticket =  urllib2.urlopen(request).read()
        print Ticket
        print len(Ticket)
    except:
        return ""

    if(len(Ticket) <> 32): return ""
    run_num = 10 #最大允许服务器错误次数
    #查询是否转换完毕
    time.sleep(5)
    while True:
        print "checkurl = " + checkurl
        if run_num < 0 :
            print "error max "
            return ""
        try:
            check_ret = checkfile(checkurl,Ticket)
        except Exception,e:
            print e
            print "checkfile error"
            run_num = run_num - 1
            time.sleep(3)
            continue
        print "check_ret = " + check_ret
        #返回码	含义	说明
        #0	正在转换过程中	已从转换队列中移除,交由转换节点开始进行转换
        #-1	数据源包不符合规范
        #文件不是ZIP文件:无法用标准ZIP方式打开文件
        #无包描述文件:无法在ZIP文件的根下找到Main.xml文件
        #包内XML文件无法解析
        #-2	找不到数据处理器	Main.xml中根节点的Type属性指定的转换处理器没有注册
        #-3	数据不可达
        #引用的内部文件无法在ZIP中找到
        #使用了外部数据,但使用提供的URL无法获取内容
        #-4	转换器错误	转换处理器在执行过程中抛出了异常导致无法正常完成转换
        #-5	转换未开始	任务正在转化队列中等待
        #-6	数据源包不存在	无法在服务器上找到指定的源数据包
        #-7	后处理错误	后处理接口在处理文件时出错
        #-8	无法读取指定模板	在数据源包或服务器上未能找到指定的模板文件
        #-9	未知错误	原因不明的任务失败,需要保留错误日志以供排查
        try:
            ret_num = int(check_ret)
            if ret_num <> -5 and ret_num <> 0:
                return ""
        except:
            print check_ret[0:4]
            if not check_ret[0:4] == "http":
                print "check_ret error , not http"
                return ""
            return Ticket
        time.sleep(3)





def checkfile(checkurl,Ticket):
    import urllib2
    print "checkurl + Ticket = " + checkurl + Ticket
    response = urllib2.urlopen(checkurl+Ticket)
    htmls = response.read()
    print "htmls = " + htmls
    return htmls




def write_ofdmeta_xml(xml_path,DocID,title, Author, Subject, Abstract, ModDate, DocUsage, Keywords, CustomDatas):
    impl = xml.dom.minidom.getDOMImplementation()
    doc = minidom.Document()
    dom = impl.createDocument(None, 'MetaRoot', None)
    root = dom.documentElement
    root.setAttribute("xmlns:xs", "http://www.w3.org/2001/XMLSchema-instance")
    root.setAttribute("xs:SchemaLocation", "metadata.xsd")

    DocIDdom = dom.createElement('DocID')
    DocIDTEXT = doc.createTextNode(DocID)
    DocIDdom.appendChild(DocIDTEXT)
    root.appendChild(DocIDdom)

    titledom = dom.createElement('Title')
    TitleTEXT = doc.createTextNode(title)
    titledom.appendChild(TitleTEXT)
    root.appendChild(titledom)

    Authordom = dom.createElement('Author')
    AuthorTEXT = doc.createTextNode(Author)
    Authordom.appendChild(AuthorTEXT)
    root.appendChild(Authordom)

    Subjectdom = dom.createElement('Subject')
    SubjectTEXT = doc.createTextNode(Subject)
    Subjectdom.appendChild(SubjectTEXT)
    root.appendChild(Subjectdom)

    Abstractdom = dom.createElement('Abstract')
    AbstractTEXT = doc.createTextNode(Abstract)
    Abstractdom.appendChild(AbstractTEXT)
    root.appendChild(Abstractdom)

    ModDatedom = dom.createElement('ModDate')
    ModDateTEXT = doc.createTextNode(ModDate)
    ModDatedom.appendChild(ModDateTEXT)
    root.appendChild(ModDatedom)

    DocUsagedom = dom.createElement('DocUsage')
    DocUsageTEXT = doc.createTextNode(DocUsage)
    DocUsagedom.appendChild(DocUsageTEXT)
    root.appendChild(DocUsagedom)

    Keywordsdom = dom.createElement('Keywords')

    for Keyword in Keywords:
        Keyworddom =  dom.createElement('Keyword')
        KeywordTEXT = doc.createTextNode(Keyword)
        Keyworddom.appendChild(KeywordTEXT)
        Keywordsdom.appendChild(Keyworddom)

    root.appendChild(Keywordsdom)

    CustomDatasdom = dom.createElement('CustomDatas')

    for (Customname,Customvalue) in CustomDatas.items():
        Customdom = dom.createElement('CustomData')
        CustomnameTEXT = doc.createTextNode(Customvalue)
        Customdom.appendChild(CustomnameTEXT)
        Customdom.setAttribute("Name",Customname)
        CustomDatasdom.appendChild(Customdom)

    root.appendChild(CustomDatasdom)

    f = open(xml_path, 'w')
    dom.writexml(f, addindent=' ', newl='\n', encoding='UTF-8')
    f.close()


def write_ofdmain_xml(xml_path, title, filename):
    impl = xml.dom.minidom.getDOMImplementation()
    doc = minidom.Document()
    dom = impl.createDocument(None, 'FileRoot', None)
    root = dom.documentElement
    root.setAttribute("Type", "wenjian.tongyong")
    root.setAttribute("xmlns:xs", "http://www.w3.org/2001/XMLSchema-instance")
    root.setAttribute("xs:SchemaLocation", "packagefile.xsd")

    Metadata = dom.createElement('Metadata')

    MetadataTEXT = doc.createTextNode("Meta.xml")
    Metadata.appendChild(MetadataTEXT)

    root.appendChild(Metadata)

    DocBody = dom.createElement('DocBody')
    root.appendChild(DocBody)

    Component = dom.createElement('Component')
    Component.setAttribute("ID", "1")
    DocBody.appendChild(Component)

    File = dom.createElement('File')
    File.setAttribute("Title", title)

    fname2 = os.path.splitext(filename)[1]
    fname2 = fname2.lower()
    fname2 = fname2[1:len(fname2)]
    File.setAttribute("Format", fname2)

    Component.appendChild(File)

    FileLoc = dom.createElement('FileLoc')
    FileLocTEXT = doc.createTextNode(filename)
    FileLoc.appendChild(FileLocTEXT)

    File.appendChild(FileLoc)

    f = open(xml_path, 'w')
    dom.writexml(f, addindent=' ', newl='\n', encoding='UTF-8')
    f.close()
    return 0

#write_ofdmain_xml("C:\\test\\main1.xml","filetitle","/Files/123.doc")

#doctoofd()

filepath = "/home/testofd/123.doc"
title = "测试文档-001"
Author = "zeus"
Subject = "测试上传的文档"
Abstract = "测试中的文档"
ModDate = "2015-07-08"
DocUsage = "颐东公司内部"
Keywords = ["测试", "颐东", "ZEUS", "过去"]
CustomDatas = {"secret_level":"1","serial_num":"new1","create_time":"20150708 12:09:01","code":"0200059"}
uuidtext = str(uuid.uuid5(uuid.NAMESPACE_DNS,title))
uuidtext = uuidtext.split('-')
uuidtext=''.join(uuidtext)
uploadurl = "http://192.168.10.187:8080/cpcns-convert-server/upload"
checkurl = "http://192.168.10.187:8080/cpcns-convert-server/query?ticket="
savepath = "C:\\Convert\\target\\"
#checkfile(checkurl,"8d7a97b55ab146e8b53f764cb66fc1c3")

filetoofd(filepath,uuidtext ,title, Author, Subject, Abstract, ModDate, DocUsage, Keywords, CustomDatas,uploadurl ,checkurl,savepath)




