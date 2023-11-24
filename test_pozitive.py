import yaml
from checkers import checkout, getout, ssh_checkout

with open('venv/config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self):
        # test1 a - sozdan archiv; v papke out proverili nalichie archiva
        result1 = checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok")
        result2 = checkout("ls {}".format(data["folder_out"]), "arx2.7z")
        assert result1 and result2, 'test1 FAIL'

    def test_step2(self, clear_folders, make_files):
        # test2
        result = []
        result.append(checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        result.append(checkout("cd {}; 7z e arx2.7z -o{} -y".format(data["folder_out"], data["folder_ext"]),
                               "Everything is Ok"))
        for item in make_files:
            result.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(result), 'test2 FAIL'

    def test_step3(self):
        # test3
        assert checkout("cd {}; 7z t arx2.7z".format(data["folder_out"]), "Everything is Ok"), 'test3 FAIL'

    def test_step4(self):
        # test4
        assert checkout("cd {}; 7z u arx2.7z".format(data["folder_in"]), "Everything is Ok"), 'test4 FAIL'

    def test_step5(self, clear_folders, make_files):
        # test5
        result = []
        result.append(checkout("cd {}; 7z a {}/arx2".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        for item in make_files:
            result.append(checkout("cd {}; 7z l arx2.7z".format(data["folder_out"], data["folder_ext"]), item))
        assert all(result), 'test5 FAIL'

   # def test_step6(self,clear_folders, make_files, make_subfolder):
        # test6
        #result = []
        #result.append(checkout("cd {}; 7z a {}/arx".format(data["folder_in"], data["folder_out"]), "Everything is Ok"))
        #result.append(checkout("cd {}; 7z x arx.7z -o{} -y".format(data["folder_out"], data["folder_ext2"]), "Everything is Ok"))
        #for item in make_files:
        #    result.append(checkout("ls {}".format(data["folder_ext2"]), item))
        #result.append(checkout("ls {}".format(data["folder_ext2"]), make_subfolder[0]))
        #result.append(checkout("ls {}/{}".format(data["folder_ext2"], make_subfolder[0]), make_subfolder[1]))
        #assert all(result), 'test6 FAIL'

    def test_step7(self):
        # test7
        assert checkout("cd {}; 7z d arx2.7z".format(data["folder_out"]), "Everything is Ok"), 'test7 FAIL'

    def test_step8(self, clear_folders, make_files):
        # test8
        result = []
        for item in make_files:
            result.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            result.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), hash))
        assert all(result), 'test8 FAIL'
