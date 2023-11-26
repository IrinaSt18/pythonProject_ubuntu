import random
import string

import pytest
import yaml
from checkers import checkout, ssh_checkout, ssh_get, ssh_checkout_negative
from datetime import datetime

from files import upload_files

with open('venv/config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                              subfoldername,
                                                                                              testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture(autouse=True)
def save_log(make_log_file, start_time):
    with open('/home/user2/logs.txt', 'w') as f:
        f.write(ssh_get("0.0.0.0", "user2", "2222", "journalctl --since {}".format(start_time), ""))




@ pytest.fixture()

def make_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "mkdir -p {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                      data["folder_ext2"]),"")


@pytest.fixture(autouse=True, scope="class")
def make_files():
    list_of_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("0.0.0.0", "user2", "2222",
                        "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename),
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope="module")
def make_log_file():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "echo '2222' | sudo -S touch /home/user2/logs.txt",
                        "")


@pytest.fixture(autouse=True, scope="module")
def clear_folders():
    return ssh_checkout("0.0.0.0", "user2", "2222",
                        "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                            data["folder_ext2"]), "")


@pytest.fixture()
def make_bad_arx():
    result1 = ssh_checkout_negative("0.0.0.0", "user2", "2222", "cd {} && echo '2222' | sudo -S 7z a {}/bad_arx".format(data["folder_in"], data["folder_out"]),
                 "Everything is Ok")
    result2 = ssh_checkout_negative("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")
    assert result1 and result2,"Failed to create bad_arx"




# Код вашей функции ssh_checkout

def make_bad_arx2():
    # Первая команда
    result1 = ssh_checkout("0.0.0.0", "user2", "2222",
                           "cd {} && echo '2222' | sudo -S 7z a {}/bad_arx".format(data["folder_in"],
                                                                                   data["folder_out"]),
                           "Everything is Ok")

    print("Result1:", result1)

    # Вторая команда
    result2 = ssh_checkout("0.0.0.0", "user2", "2222", "truncate -s 1 {}/bad_arx.7z".format(data["folder_out"]), "")

    print("Result2:", result2)

    # Проверяем результаты и выводим дополнительные отладочные сообщения
    if result1:
        print("First command successful.")
    else:
        print("Error in the first command.")

    if result2:
        print("Second command successful.")
    else:
        print("Error in the second command.")

    assert result1 and result2, "Failed to create bad_arx"





@pytest.fixture(autouse=True, scope="module")
def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "2222", "/home/user/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "2222", "echo '2222' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Status: install ok installed"))
    return all(res)
