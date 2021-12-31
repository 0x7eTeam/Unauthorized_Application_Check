# coding=utf-8
import ftplib, threading, requests, pymongo, pymysql,socket,sys
import psycopg2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

R = threading.Lock()


def echoMessage():
    version = """  
      [#] Create By ::
        _                     _    ___   __   ____                             
       / \   _ __   __ _  ___| |  / _ \ / _| |  _ \  ___ _ __ ___   ___  _ __  
      / _ \ | '_ \ / _` |/ _ \ | | | | | |_  | | | |/ _ \ '_ ` _ \ / _ \| '_ \ 
     / ___ \| | | | (_| |  __/ | | |_| |  _| | |_| |  __/ | | | | | (_) | | | |
    /_/   \_\_| |_|\__, |\___|_|  \___/|_|   |____/ \___|_| |_| |_|\___/|_| |_|
                   |___/            By https://aodsec.com                                           
    """
    print(version)

def file_write(file_name,text):
    global R
    R.acquire()
    f = open(file_name, 'a', encoding='utf-8').write(text + '\n')
    R.release()


def redis(ip):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 6379))
        s.send(bytes("INFO\r\n", 'UTF-8'))
        result = s.recv(1024).decode()
        if "redis_version" in result:
            # print(ip + ":6379 redis未授权")
            file_write("redis.txt",ip + ":6379 redis未授权")
        s.close()
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


def mongodb(ip):
    try:
        conn = pymongo.MongoClient(ip, 27017, socketTimeoutMS=4000)
        dbname = conn.list_database_names()
        # print(ip + ":27017 mongodb未授权")
        file_write("mongodb.txt",ip + ":27017 mongodb未授权")
        conn.close()
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


def memcached(ip):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 11211))
        s.send(bytes('stats\r\n', 'UTF-8'))
        if 'version' in s.recv(1024).decode():
            print(s.recv(2048).decode())
            # print(ip + ":11211 memcached未授权")
            file_write("memcached.txt",ip + ":11211 memcached未授权")
        s.close()
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def elasticsearch(ip):
    try:
        url = 'http://' + ip + ':9200/_cat'
        r = requests.get(url, timeout=5)
        if '/_cat/master' in r.content.decode():
            # print(ip + ":9200 elasticsearch未授权")
            file_write("elasticsearch.txt",ip + ":9200 elasticsearch未授权")
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


def zookeeper(ip):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 2181))
        s.send(bytes('envi', 'UTF-8'))
        data = s.recv(1024).decode()
        s.close()
        if 'Environment' in data:
            # print(ip + ":2181 zookeeper未授权")
            file_write("zookeeper.txt",ip + ":2181 zookeeper未授权")
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


def ftp(ip):
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, 21, timeout=5)  # 连接的ftp sever和端口
        ftp.login('anonymous', 'Aa@12345678')
        # print(str(ip) + ":21 FTP未授权")
        file_write("ftp.txt",str(ip) + ":21 FTP未授权")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def CouchDB(ip):
    try:
        url = 'http://' + ip + ':5984' + '/_utils/'
        r = requests.get(url, timeout=5)
        if 'couchdb-logo' in r.content.decode():
            # print(ip + ":5984 CouchDB未授权")
            file_write("CouchDB.txt",ip + ":5984 CouchDB未授权")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def docker(ip):
    try:
        url = 'http://' + ip + ':2375' + '/version'
        r = requests.get(url, timeout=5)
        if 'ApiVersion' in r.content.decode():
            # print(ip + ":2375 docker api未授权")
            file_write("docker.txt",ip + ":2375 docker api未授权")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def Hadoop(ip):
    try:
        url = 'http://' + ip + ':50070' + '/dfshealth.html'
        r = requests.get(url, timeout=5)
        if 'hadoop.css' in r.content.decode():
            # print(ip + ":50070 Hadoop未授权")
            file_write("Hadoop.txt",ip + ":50070 Hadoop未授权")
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


def rsync_access(ip):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 873))
        s.send(bytes("", 'UTF-8'))
        result = s.recv(1024).decode()
        print(result)
        if "RSYNCD" in result:
            # print(ip + ":873 可能存在rsync未授权,需要手工确认")
            file_write("rsync_access.txt",ip + ":873 可能存在rsync未授权,需要手工确认")
        s.close()
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def mysql_Empty_pwd(ip):
    try:
        conn = pymysql.connect(host=ip, user='root', password='', charset='utf8', autocommit=True)
        # print(ip + ":3306 存在mysql空口令漏洞")
        file_write("mysql_Empty_pwd.txt",ip + ":3306 存在mysql空口令漏洞")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def jenkins(ip):
    try:
        url = 'http://' + ip + ':8080' + '/systemInfo'
        r = requests.get(url, timeout=8, verify=False)
        if 'jenkins.war' in r.content.decode() and 'JENKINS_HOME' in r.content.decode():
            # print(ip + ":8080 发现jenkins 未授权")
            file_write("jenkins.txt",ip + ":8080 发现jenkins 未授权")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def jboss(ip):
    try:
        url = 'http://' + ip + ':8080' + '/jmx-console/HtmlAdaptor?action=displayMBeans'
        r = requests.get(url, timeout=8, verify=False)
        if 'JBoss JMX Management Console' in r.content.decode() and r.status_code == 200 and 'jboss' in r.content.decode():
            # print(ip + ":8080 发现jboss未授权访问")
            file_write("jboss.txt",ip + ":8080 发现jboss未授权访问")
    except Exception as e:
        pass
    finally:
        pass
        bar.update(1)


def postgres(ip):
    try:
        conn = psycopg2.connect(database="postgres", user="postgres", password="", host=ip, port="5432")
        # print(ip + ":5432 存在postgres未授权")
        file_write("postgres.txt",ip + ":5432 存在postgres未授权")
    except Exception as e:
        # print(e)
        pass
    finally:
        pass
        bar.update(1)


if __name__ == '__main__':
    echoMessage()
    choice ="# 目前支持：redis,Hadoop,docker,CouchDB,ftp,zookeeper,elasticsearch,memcached,mongodb,rsync_access,mysql,target,jenkins,target,jboss的未授权访问，检测速度快" 
    print(choice)
    if len(sys.argv) < 2:
        print("usage:\n\tpython3 aodsec_search.py [redis|mongodb|...] ip.txt thread_num")
    else:
        ip_txt = sys.argv[2]
        type_scan = sys.argv[1]
        if type_scan not in choice:
            print("请输出正确的选项")
            sys.exit()
        ipfile = open(ip_txt, 'r', encoding='utf-8').read().split('\n')
        bar = tqdm(total=len(ipfile) * 10)
        pool = ThreadPoolExecutor(int(sys.argv[3]))
        for target1 in ipfile:
            target2 = target1.strip().replace("http://","")
            if ":" in target2:
                target = target2[:target2.index(":")]
            else:
                target = target2
            if(type_scan=="redis"):
                pool.submit(redis, target)
            elif(type_scan=="Hadoop"):
                pool.submit(Hadoop, target)
            elif(type_scan=="docker"):
                pool.submit(docker, target)
            elif(type_scan=="CouchDB"):
                pool.submit(CouchDB, target)
            elif(type_scan=="ftp"):
                pool.submit(ftp, target)
            elif(type_scan=="zookeeper"):
                pool.submit(zookeeper, target)
            elif(type_scan=="elasticsearch"):
                pool.submit(elasticsearch, target)
            elif(type_scan=="memcached"):
                pool.submit(memcached, target)
            elif(type_scan=="mongodb"):
                pool.submit(mongodb, target)
            elif(type_scan=="rsync_access"):
                pool.submit(rsync_access, target)
            elif(type_scan=="mysql_Empty_pwd"):
                pool.submit(mysql_Empty_pwd, target)
            elif(type_scan=="jenkins"):
                pool.submit(jenkins, target)
            elif(type_scan=="jboss"):
                pool.submit(jboss, target)
            elif(type_scan=="postgres"):
                pool.submit(postgres, target)
            else:
                pass
