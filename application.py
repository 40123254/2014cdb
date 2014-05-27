#@+leo-ver=5-thin
#@+node:course-mde-tw.20140417093332.2028: * @file application
#@@language python
#@@tabwidth -4
#@+others
#@+node:course-mde-tw.20140417093332.2029: ** declarations

########################### 1. 導入所需模組
import cherrypy
import os
import cmsimply

########################### 2. 設定近端與遠端目錄
# 確定程式檔案所在目錄, 在 Windows 有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"

#@+node:course-mde-tw.20140417093332.2030: ** class CDProject
########################### 3. 建立主物件
class CDProject(object):
    _cp_config = {
    # if there is no utf-8 encoding, no Chinese input available
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session timeout is 60 minutes
    'tools.sessions.timeout' : 60
    }
    
    #@+others
    #@+node:course-mde-tw.20140417093332.2031: *3* __init__
    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
        if not os.path.isdir(data_dir+"brython_programs"):
            try:
                os.makedirs(data_dir+"brython_programs")
            except:
                print("mkdir error")
        if not os.path.isdir(data_dir+"calc_programs"):
            try:
                os.makedirs(data_dir+"calc_programs")
            except:
                print("mkdir error")

    #@+node:course-mde-tw.20140417093332.2032: *3* index
    @cherrypy.expose
    def index(self, input1=None, input2=None):
        raise cherrypy.HTTPRedirect("/cmsimply")
        return "設定與 Github 同步"+str(input1)
    #@+node:course-mde-tw.20140417093332.2033: *3* default
    # default method, if there is no corresponding method, cherrypy will redirect to default method
    # need *args and **kwargs as input variables for all possible URL links
    @cherrypy.expose
    # default can not live with calc method?
    def default_void(self, attr='default', *args, **kwargs):
        raise cherrypy.HTTPRedirect("/")
    #@+node:course-mde-tw.20140417093332.2034: *3* save_program
    @cherrypy.expose
    def save_program(self, filename=None, sheet_content=None):
        with open(data_dir+"/calc_programs/"+filename, "wt", encoding="utf-8") as out_file:
            data = sheet_content.replace("\r\n", "\n")
            out_file.write(data)

        return str(filename)+" saved!<br />"
     





    #@+node:course-mde-tw.20140417093332.2035: *3* inputform
    @cherrypy.expose
    def inputform(self, input1=None, input2=None):
        return "input form"+str(input1)
    #@+node:course-mde-tw.20140417093332.2038: *3* print99
    @cherrypy.expose
    # version 1 use no table
    def print99(self, var1=10, var2=10):
        # initialize outstring
        outstring = ""
        # initialize count
        count = 0
        for i in range(1, int(var1)):
            for j in range(1, int(var2)):
                count += 1
                if count%9 == 0:
                    outstring += str(i) + "x" + str(j) + "=" + str(i*j) + "<br />"
                else:
                    outstring += str(i) + "x" + str(j) + "=" + str(i*j) + "&nbsp;"*4
        return outstring
        #return "列印九九乘法表"+str(var1)+str(var2)
    #@+node:course-mde-tw.20140417093332.2039: *3* print992
    @cherrypy.expose
    # version 2 use table
    def print992(self, var1=10, var2=10):
        # initialize outstring
        outstring = "<table  style='border: 5px double rgb(109, 2, 107); height: 100px; background-color: rgb(255, 255, 255); width: 300px;' align='left' cellpadding='8' cellspacing='8' frame='border' rules='all'>"
        # initialize count
        count = 0
        for i in range(1, int(var1)):
            outstring += "<tr>"
            for j in range(1, int(var2)):
                outstring += "<td>"+str(i) + "x" + str(j) + "=" + str(i*j) + "</td>"
            outstring += "</tr>"
        outstring += "</table>"
        return outstring
        #return "列印九九乘法表"+str(var1)+str(var2)
    #@+node:course-mde-tw.20140417093332.2040: *3* print993
    @cherrypy.expose
    # version 3 add javascript alert
    def print993(self, var1=10, var2=10):
        # initialize outstring
        outstring = "<table  style='border: 5px double rgb(109, 2, 107); height: 600px; background-color: rgb(255, 255, 255); width: 800px;' align='left' cellpadding='8' cellspacing='8' frame='border' rules='all'>"
        # initialize count
        count = 0
        for i in range(1, int(var1)):
            outstring += "<tr>"
            for j in range(1, int(var2)):
                outstring += "<td><button onClick=alert('"+str(i*j)+"')>"+str(i) + "x" + str(j) + "</button>=" + str(i*j) + "</td>"
            outstring += "</tr>"
        outstring += "</table>"
        return outstring
        #return "列印九九乘法表"+str(var1)+str(var2)
    #@-others
    #index.exposed = True

#@-others
########################### 4. 安排啟動設定
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {
        '/static':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': _curdir+"/static"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/brython_programs':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/brython_programs"},
        '/calc_programs':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/calc_programs"},
        '/':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': _curdir+"/static/openjscad"}
    }

########################### 5. 在近端或遠端啟動程式
# 利用 HelloWorld() class 產生案例物件
root = CDProject()
# 導入 CMSimply 內容管理模組
root.cmsimply = cmsimply.CMSimply()
# 導入 Download
root.cmsimply.download = cmsimply.Download()
#####################################################
# 導入協同程式 cdbg1
#####################################################
# 以下為 cdbg1 的模組導入與連結設定
import programs.cdbg1 as cdbg1
root.cdbg1 = cdbg1.CDBG1()
#####################################################
# 導入協同程式 cdbg2
#####################################################
# 以下為 cdbg2 的模組導入與連結設定
import programs.cdbg2 as cdbg2
root.cdbg2 = cdbg2.CDBG2()
#####################################################
# 導入協同程式 cdbg13
#####################################################
# 以下為 cdbg13 的模組導入與連結設定
import programs.cdbg13 as cdbg13
root.cdbg13 = cdbg13.CDBG13()
#####################################################
# 導入協同程式 cdbg14
#####################################################
# 以下為 cdbg14 的模組導入與連結設定
import programs.cdbg14 as cdbg14
root.cdbg14 = cdbg14.CDBG14()

# 以下為 cdbg30 的模組導入與連結設定
import programs.cdbg30 as cdbg30
root.cdbg30 = cdbg30.CDBG30()
import programs.cdbg30.man as cdbg30_man
# 加入 cdag30 模組下的 man.py 且以子模組 man 對應其 MAN() 類別
root.cdbg30.man = cdbg30_man.MAN()
import programs.cdbg30.man2 as cdbg30_man2
root.cdbg30.man2 = cdbg30_man2.MAN()
#####################################################
# 導入協同程式 cdbg9
#####################################################
# 以下為 cdbg9 的模組導入與連結設定
import programs.cdbg9 as cdbg9
root.cdbg9 = cdbg9.CDBG9()
#####################################################
# 導入協同程式 cdbg6
#####################################################
# 以下為 cdbg6 的模組導入與連結設定
import programs.cdbg6 as cdbg6
root.cdbg6 = cdbg6.CDBG6()
#####################################################
# 導入協同程式 cdbg8
#####################################################
# 以下為 cdbg8 的模組導入與連結設定
import programs.cdbg8 as cdbg8
root.cdbg8 = cdbg8.CDBG8()
# 假如在 os 環境變數中存在 'OPENSHIFT_REPO_DIR', 表示程式在 OpenShift 環境中執行
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 雲端執行啟動
    application = cherrypy.Application(root, config = application_conf)
else:
    # 近端執行啟動
    '''
    cherrypy.server.socket_port = 8083
    cherrypy.server.socket_host = '127.0.0.1'
    '''
    cherrypy.quickstart(root, config = application_conf)
#@-leo
