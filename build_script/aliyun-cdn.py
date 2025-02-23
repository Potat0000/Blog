#!/usr/bin/env python3
# coding=utf-8

import getopt, json, logging, re, sys, time
from aliyunsdkcdn.request.v20180510.DescribeRefreshQuotaRequest import DescribeRefreshQuotaRequest
from aliyunsdkcdn.request.v20180510.DescribeRefreshTasksRequest import DescribeRefreshTasksRequest
from aliyunsdkcdn.request.v20180510.PushObjectCacheRequest import PushObjectCacheRequest
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest
from aliyunsdkcore.client import AcsClient

# 初始化日志记录
logging.basicConfig(level=logging.DEBUG, filename='./RefreshAndPredload.log')


# 定义全局变量类，存储AK、SK、FD等信息
class Envariable(object):
    LISTS = []
    REGION = 'cn-zhangzhou'
    AK = None
    SK = None
    FD = None
    CLI = None
    TASK_TYPE = None
    TASK_AREA = None
    TASK_OTYPE = None

    # 设置AK
    @staticmethod
    def set_ak(ak):
        Envariable.AK = ak

    # 获取AK
    @staticmethod
    def get_ak():
        return Envariable.AK

    # 设置SK
    @staticmethod
    def set_sk(sk):
        Envariable.SK = sk

    # 获取SK
    @staticmethod
    def get_sk():
        return Envariable.SK

    # 设置FD
    @staticmethod
    def set_fd(fd):
        Envariable.FD = fd

    # 获取FD
    @staticmethod
    def get_fd():
        return Envariable.FD

    # 设置任务类型
    @staticmethod
    def set_task_type(task_type):
        Envariable.TASK_TYPE = task_type

    # 获取任务类型
    @staticmethod
    def get_task_type():
        return Envariable.TASK_TYPE

    # 设置任务区域
    @staticmethod
    def set_task_area(task_area):
        Envariable.TASK_AREA = task_area

    # 获取任务区域
    @staticmethod
    def get_task_area():
        return Envariable.TASK_AREA

    # 设置任务对象类型
    @staticmethod
    def set_task_otype(task_otype):
        Envariable.TASK_OTYPE = task_otype

    # 获取任务对象类型
    @staticmethod
    def get_task_otype():
        return Envariable.TASK_OTYPE

    # 创建AcsClient
    @staticmethod
    def set_acs_client():
        Envariable.CLI = AcsClient(Envariable.get_ak(), Envariable.get_sk(), Envariable.REGION)

    # 获取AcsClient
    @staticmethod
    def get_acs_client():
        return Envariable.CLI


class InitHandler(object):
    def __init__(self, ak, sk, region):
        try:
            self.client = AcsClient(ak, sk, region)
        except Exception:
            logging.info('[error]: initial AcsClient failed')
            exit(1)


class BaseCheck(object):
    def __init__(self):
        self.invalidurl = ''
        self.lines = 0
        self.urllist = Envariable.get_fd()

    # 检查配额
    def printQuota(self):
        try:
            if Envariable.get_acs_client():
                client = Envariable.get_acs_client()
            else:
                Envariable.set_acs_client()
                client = Envariable.get_acs_client()
            quotas = DescribeRefreshQuotaRequest()
            quotaResp = json.loads(client.do_action_with_exception(quotas))
        except Exception:
            logging.info('\n[error]: initial AcsClient failed\n')
            sys.exit(1)

        if Envariable.TASK_TYPE:
            if Envariable.TASK_TYPE == 'push':
                if self.lines > int(quotaResp['PreloadRemain']):
                    sys.exit('\n[error]：PreloadRemain is not enough {0}'.format(quotaResp['PreloadRemain']))
                return True
            if Envariable.TASK_TYPE == 'clear':
                if Envariable.get_task_otype() == 'File' and self.lines > int(quotaResp['UrlRemain']):
                    sys.exit('\n[error]：UrlRemain is not enough {0}'.format(quotaResp['UrlRemain']))
                elif Envariable.get_task_otype() == 'Directory' and self.lines > int(quotaResp['DirRemain']):
                    sys.exit('\n[error]：DirRemain is not enough {0}'.format(quotaResp['DirRemain']))
                else:
                    return True

    # 验证URL格式
    def urlFormat(self):
        with open(self.urllist, 'r') as f:
            for line in f.readlines():
                self.lines += 1
                if not re.match(r'^((https)|(http))', line):
                    self.invalidurl = line + '\n' + self.invalidurl
            if self.invalidurl != '':
                sys.exit('\n[error]: URL format is illegal \n{0}'.format(self.invalidurl))
            return True


# 批量处理类，将URL列表按指定数量分成多个批次
class doTask(object):
    @staticmethod
    def urlencode_pl(inputs_str):
        len_str = len(inputs_str)
        if inputs_str == '' or len_str <= 0:
            return ''
        result_end = ''
        for chs in inputs_str:
            if chs.isalnum() or chs in {':', '/', '.', '-', '_', '*'}:
                result_end += chs
            elif chs == ' ':
                result_end += '+'
            else:
                result_end += f'%{ord(chs):02X}'
        return result_end

    # 分批处理URL
    @staticmethod
    def doProd():
        gop = 20  # 这里定义了每个批次的最大URL数量
        mins = 1
        maxs = gop
        with open(Envariable.get_fd(), 'r') as f:
            for line in f.readlines():
                line = doTask.urlencode_pl(line.strip()) + '\n'
                Envariable.LISTS.append(line)
                if mins >= maxs:
                    yield Envariable.LISTS
                    Envariable.LISTS = []
                    mins = 1
                else:
                    mins += 1
        if Envariable.LISTS:
            yield Envariable.LISTS

    # 执行刷新或预热任务
    @staticmethod
    def doRefresh(lists):
        try:
            if Envariable.get_acs_client():
                client = Envariable.get_acs_client()
            else:
                Envariable.set_acs_client()
                client = Envariable.get_acs_client()

            if Envariable.get_task_type() == 'clear':
                taskID = 'RefreshTaskId'
                request = RefreshObjectCachesRequest()
                if Envariable.get_task_otype():
                    request.set_ObjectType(Envariable.get_task_otype())
            elif Envariable.get_task_type() == 'push':
                taskID = 'PushTaskId'
                request = PushObjectCacheRequest()
                if Envariable.get_task_area():
                    request.set_Area(Envariable.get_task_area())

            taskreq = DescribeRefreshTasksRequest()
            request.set_accept_format('json')
            request.set_ObjectPath(lists)
            response = json.loads(client.do_action_with_exception(request))
            print(response)

            timeout = 0
            while True:
                count = 0
                taskreq.set_accept_format('json')
                taskreq.set_TaskId(response[taskID])
                taskresp = json.loads(client.do_action_with_exception(taskreq))
                print(f'[{response[taskID]}] is doing... ...')
                for t in taskresp['Tasks']['CDNTask']:
                    if t['Status'] != 'Complete':
                        count += 1
                if count == 0:
                    logging.info(f'[{response[taskID]}] is finish')
                    break
                elif timeout > 5:
                    logging.info(f'[{response[taskID]}] timeout')
                    break
                else:
                    timeout += 1
                    time.sleep(5)
                    continue
        except Exception as e:
            logging.info(f'\n[error]：{e}')
            sys.exit(1)


class Refresh(object):
    def main(self, argv):
        if len(argv) < 1:
            sys.exit(f'\n[usage]: {sys.argv[0]} -h ')
        try:
            opts, args = getopt.getopt(argv, 'hi:k:n:r:t:a:o:')
        except getopt.GetoptError:
            sys.exit(f'\n[usage]: {sys.argv[0]} -h ')

        for opt, arg in opts:
            if opt == '-h':
                self.help()
                sys.exit()
            elif opt == '-i':
                Envariable.set_ak(arg)
            elif opt == '-k':
                Envariable.set_sk(arg)
            elif opt == '-r':
                Envariable.set_fd(arg)
            elif opt == '-t':
                Envariable.set_task_type(arg)
            elif opt == '-a':
                Envariable.set_task_area(arg)
            elif opt == '-o':
                Envariable.set_task_otype(arg)
            else:
                sys.exit(f'\n[usage]: {sys.argv[0]} -h ')

        try:
            if not (Envariable.get_ak() and Envariable.get_sk() and Envariable.get_fd() and Envariable.get_task_type()):
                sys.exit("\n[error]: Must be by parameter '-i', '-k', '-r', '-t'\n")
            if Envariable.get_task_type() not in {'push', 'clear'}:
                sys.exit("\n[error]: taskType Error, '-t' option in 'push' or 'clear'\n")
            if Envariable.get_task_area() and Envariable.get_task_otype():
                sys.exit('\n[error]: -a and -o cannot exist at same time\n')
            if Envariable.get_task_area():
                if Envariable.get_task_area() not in {'domestic', 'overseas'}:
                    sys.exit("\n[error]: Area value Error, '-a' option in 'domestic' or 'overseas'\n")
            if Envariable.get_task_otype():
                if Envariable.get_task_otype() not in {'File', 'Directory'}:
                    sys.exit("\n[error]: ObjectType value Error, '-a' options in 'File' or 'Directory'\n")
                if Envariable.get_task_type() == 'push':
                    sys.exit("\n[error]: -t must be clear and 'push' -a use together\n")
        except Exception as e:
            logging.info(f'\n[error]: Parameter {e} error\n')
            sys.exit(1)

        handler = BaseCheck()
        if handler.urlFormat() and handler.printQuota():
            for g in doTask.doProd():
                doTask.doRefresh(''.join(g))
                time.sleep(1)

    def help(self):
        print(
            '\nscript options explain: \
                    \n\t -i <AccessKey>                  访问阿里云凭证，访问控制台上可以获得； \
                    \n\t -k <AccessKeySecret>            访问阿里云密钥，访问控制台上可以获得； \
                    \n\t -r <filename>                   filename指“文件所在的路径+文件名称”，自动化脚本运行后将会读取文件内记录的URL；文件内的URL记录方式为每行一条URL，有特殊字符先做URLencode，以http或https开头； \
                    \n\t -t <taskType>                   任务类型，clear：刷新，push：预热； \
                    \n\t -a [String,<domestic|overseas>] 可选项，预热范围，不传默认是全球；\
                    \n\t    domestic                     仅中国内地； \
                    \n\t    overseas                     全球（不包含中国内地）； \
                    \n\t -o [String,<File|Directory>]    可选项，刷新的类型； \
                    \n\t    File                         文件刷新（默认值）； \
                    \n\t    Directory                    目录刷新'
        )


if __name__ == '__main__':
    fun = Refresh()
    fun.main(sys.argv[1:])
