import unittest
from pyfoundt.pyfoundt import set_plt

te = 1
set_plt.xin_jian_file("c:/ll.txt")
set_plt.xin_jian_file("c:/l.txt")
pip = set_plt.PipOperation()
pip.uninstall("numpy", "c:/")
pip.install("numpy", "c:/")
pip.upgrade_pip("c:/")
pip.pip_list("c:/")


class TestSetPlt(unittest.TestCase):
    def test_xin_jian_file(self):
        try:
            with open("c:/ll.txt", "r") as f:
                f.close()
        except Exception:
            self.assertEqual(te, 2)
        else:
            self.assertEqual(te, 1)
            f.close()

    def test_return_file_info(self):
        l = set_plt.return_file_info("c:/ll.txt")
        with open("c:/ll.txt", "r") as f:
            lv = f.read()
            self.assertEqual(l, lv)
            f.close()

    def test_delete(self):
        set_plt.delete("c:/l.txt")
        try:
            with open("c:/l.txt") as f:
                f.close()
        except Exception:
            self.assertEqual(te, 1)
        else:
            self.assertEqual(te, 2)
            f.close()

    def test_return_url_info(self):
        import requests
        l = set_plt.return_url_info("https://baidu.com")
        lv = requests.get("https://baidu.com").text
        self.assertEqual(l, lv)

    def test_get_url_Infile(self):
        import requests
        set_plt.get_url_Infile("https://baidu.com")
        r = requests.get("https://baidu.com")
        r.encoding = "utf-8"
        with open("c:/n.html", "wb") as f:
            f.write(r.content)
        try:
            with open("c:/.html", "r", encoding="utf-8") as f:
                rv = f.read()
                f.close()
            with open("c:/n.html", "r") as f:
                rvv = f.read()
                f.close()
        except UnicodeDecodeError:
            self.assertEqual(te, 1)
        else:
            self.assertEqual(rv, rvv)


class TestPipOperation(unittest.TestCase):
    def test_install(self):
        try:
            with open("c:/install -numpy.bat", "r"):
                print()
        except FileNotFoundError:
            self.assertEqual(te, 2)
        else:
            self.assertEqual(te, 1)

    def test_uninstall(self):
        try:
            with open("c:/uninstall -numpy.bat", "r"):
                print()
        except FileNotFoundError:
            self.assertEqual(te, 2)
        else:
            self.assertEqual(te, 1)

    def test_upgrade_pip(self):
        try:
            with open("c:/upgrade pip.bat", "r"):
                print()
        except FileNotFoundError:
            self.assertEqual(te, 2)
        else:
            self.assertEqual(te, 1)

    def test_pip_list(self):
        try:
            with open("c:/pip_list.bat", "r"):
                print()
        except FileNotFoundError:
            self.assertEqual(te, 2)
        else:
            self.assertEqual(te, 1)


class TestTime(unittest.TestCase):
    def test_now(self):
        from datetime import datetime
        time = set_plt.Time
        n = time.now(detailed=True)
        nv = datetime.now()
        self.assertEqual(n, nv)


if __name__ == "__main__":
    unittest.main()
