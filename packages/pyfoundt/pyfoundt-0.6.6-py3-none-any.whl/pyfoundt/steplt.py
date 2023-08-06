import os
import requests


def return_file_info(file, encoding="utf-8"):
    """
    :param file: 打印内容的文件名
    :param encoding: 编码
    :return: fv
    """
    f = None
    try:
        f = open(f"{file}", "r", encoding=encoding)
        for fv in f:
            return fv
    finally:
        if f is not None:
            f.close()


def xin_jian_file(file, data="", encoding="utf-8"):
    """
    :param file: 创建的文件名
    :param data: 写入内容
    :param encoding:编码
    :return: None
    """
    f = None
    try:
        with open(f"{file}", "a", encoding=encoding) as f:
            f.write(data)
    finally:
        if f is not None:
            f.close()

        else:
            try:
                with open(f"{file}", "a", encoding=encoding) as f:
                    f.write(data)
            finally:
                if f is not None:
                    f.close()


def return_url_info(url):
    r = requests.get(url)
    return r.text


def get_url_Infile(url, file="c:/.html"):
    """
    :param url: 爬取的链接
    :param file: 存入的文件名称
    :return: None
    """
    r = requests.get(url)
    with open(file, "wb") as f:
        f.write(r.content)


def delete(file):
    """
    :param file: 删除文件名称
    :return: None
    """
    os.remove(f"{file}")


class PipOperation(object):
    """
    作用：pip的常用操作
    属性：None
    """

    @staticmethod
    def install(modular, luj=None):
        """
        :param modular: 要安装的模块
        :param luj: 安装包的路径
        :return: None
        """
        if luj is None:
            with open(f"install -{modular}.bat", "a") as f:
                f.write(f"pip install {modular} -i https://mirror.baidu.com/pypi/simple")
        else:
            with open(f"{luj}install -{modular}.bat", "a") as f:
                f.write(f"pip install {modular} -i https://mirror.baidu.com/pypi/simple")

    @staticmethod
    def uninstall(modular, luj=None):
        """
        :param modular: 卸载的模块
        :param luj: 卸载包的路径
        :return: None
        """
        if luj is None:
            with open(f"uninstall -{modular}.bat", "a") as f:
                f.write(f"pip uninstall {modular}")
        else:
            with open(f"{luj}uninstall -{modular}.bat", "a") as f:
                f.write(f"pip uninstall {modular}")

    @staticmethod
    def upgrade_modular(modular, luj=None):
        """
        :param modular: 更新的模块
        :param luj: 更新包的路径
        :return: None
        """
        if luj is None:
            with open("upgrade pip.bat", "a") as f:
                f.write(f"pip install --upgrade {modular}")
        else:
            with open(f"{luj}upgrade pip.bat", "a") as f:
                f.write(f"pip install --upgrade {modular}")

    @staticmethod
    def pip_list(luj=None):
        """
        :param luj: 显示文件的路径
        :return: None
        """
        if luj is None:
            with open("pip_list.bat", "a") as f:
                f.write("pip list\nping 127.1 -n 6 >nul")
        else:
            with open(f"{luj}pip_list.bat", "a") as f:
                f.write("pip list\nping 127.1 -n 6 >nul")


class Time(object):
    """
    作用：记录时间 或 获取当前时间
    属性：year(年), month(月), day(天), hour(时), minute(分钟), second(秒)
    """

    def __init__(self, year=2012, month=1, day=1,
                 hour=0, minute=0, second=0):

        self.hour = hour
        self.minute = minute
        self.second = second
        self.day = day
        self.month = month
        self.year = year

        for i in range(99):
            if self.second >= 60:
                self.minute += 1
                self.second -= 60
            if self.minute >= 60:
                self.hour += 1
                self.minute -= 60
            if self.hour >= 24:
                self.hour -= 24
                self.day += 1
            if self.day >= 30:
                self.day -= 30
                self.month += 1
            if self.month == 12:
                if self.day >= 30:
                    self.year += 1
                    self.month = 1
            if self.month > 12:
                self.month = 1
                self.year += 1

    def __str__(self):
        return "%.4d-%.2d-%.2d %.2d:%.2d:%.2d" % (self.year,
                                                  self.month,
                                                  self.day,
                                                  self.hour,
                                                  self.minute,
                                                  self.second)

    def __add__(self, time1, time2):
        return time1 + time2

    @staticmethod
    def now(detailed=False):
        if detailed is False:
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        if detailed is True:
            import datetime
            now = datetime.datetime.now()
            return now


if __name__ == "__main__":
    time = Time()
    print(time)
