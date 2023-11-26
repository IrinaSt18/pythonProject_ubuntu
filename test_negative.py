import yaml

from checkers import ssh_checkout_negative

with open('venv/config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        # test1
        assert ssh_checkout_negative("0.0.0.0", "user2", "2222",
                                     "cd {}; 7z e bad_arx.7z -o{} -y".format(data["folder_out"],
                                     data["folder_ext"]),
                                     "ERRORS"), "test1 FAIL"

    def test_step2(self):
        # test2
        assert ssh_checkout_negative("0.0.0.0", "user2", "2222",
                                     "cd {} && echo '2222' | sudo -S 7z t bad_arx.7z".format(data["folder_out"]),
                                     "ERRORS"), "test2 FAIL"
