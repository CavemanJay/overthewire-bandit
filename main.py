import re
import os
import paramiko

host = "bandit.labs.overthewire.org"
ssh_port = 2220
credentials = {"bandit0": "bandit0"}

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()


def save_key(username, contents):
    next_user = get_next_user(username)
    path = f'/tmp/{next_user}_id_rsa'
    with open(path, 'w') as f:
        f.write(contents)

    os.chmod(path, 0o600)
    return [path]


def get_next_user(username: str):
    challenge = int(re.findall(r'bandit(\d+)', username)[0])
    return f'bandit{challenge+1}'


def connect(username: str, client=None):
    client = client or ssh
    creds = credentials[username]
    if isinstance(creds, str):
        client.connect(host, ssh_port, username=username, password=creds)
    else:
        if os.path.exists(creds[0]):
            client.connect(host, ssh_port, username=username,
                           key_filename=creds[0])
        else:
            client.connect(host, ssh_port, username=username,
                           password=creds[1])


def save(func):
    def _save_passwd(*args, **kwargs):
        ssh.close()
        username, passwd = func(*args, **kwargs)
        next_user = get_next_user(username)
        credentials[next_user] = passwd
        print(F"{next_user} {passwd}")

    return _save_passwd


def pwn(func):
    @save
    def exec(*args, **kwargs):
        username = func.__name__
        connect(username)
        cmd = func(*args, **kwargs)
        _, out, _ = ssh.exec_command(cmd)
        passwd = out.read().decode().strip()
        return username, passwd

    return exec


@pwn
def bandit0():
    return "cat readme"


@pwn
def bandit1():
    return r"cat ./-"


@pwn
def bandit2():
    return r'cat "spaces in this filename"'


@pwn
def bandit3():
    return r'cat ./inhere/.hidden'


@pwn
def bandit4():
    return r'file **/* | grep -i ascii | cut -d: -f1 | xargs cat'


@pwn
def bandit5():
    return r'find . -size 1033c \! -executable -exec cat {} \;'


@pwn
def bandit6():
    return r'find / -user bandit7 -group bandit6 -size 33c -exec cat {} \;'


@pwn
def bandit7():
    return r'grep millionth data.txt | xargs | cut -d " " -f2'


@pwn
def bandit8():
    return r'sort data.txt | uniq -u'


@pwn
def bandit9():
    return r'strings -n 7 data.txt | grep ^= | tail -n 1 | cut -d " " -f2'


@pwn
def bandit10():
    return r'cat data.txt | base64 -d | cut -d " " -f4'


@pwn
def bandit11():
    return r'cat data.txt | tr "A-Za-z" "N-ZA-Mn-za-m" | cut -d " " -f4'


@pwn
def bandit12():
    return '''
    mkdir /tmp/jaydlc
    cd /tmp/jaydlc
    cat ~/data.txt | xxd -r > data2.gz
    gunzip data2.gz; mv data2 data3.bz2
    bunzip2 data3.bz2; mv data3 data4.gz
    gunzip data4.gz; mv data4 data5.tar
    tar xf data5.tar; mv data5.bin data6.tar; rm data5.tar
    tar xf data6.tar; mv data6.bin data7.bz2; rm data6.tar
    bunzip2 data7.bz2; mv data7 data8.tar
    tar xf data8.tar; mv data8.bin data9.gz; rm data8.tar
    gunzip data9.gz
    cat data9 | cut -d " " -f4
    rm -rf /tmp/jaydlc/*
    '''.replace("\n", ";").removeprefix(";").strip()


@save
def bandit13():
    username = "bandit13"
    connect(username)
    _, out, _ = ssh.exec_command("cat ./sshkey.private")
    key = out.read().decode()
    return username, save_key(username, key)


@save
def bandit14():
    username = "bandit14"
    connect(username)
    pass_file = "/etc/bandit_pass/bandit14"
    _, out, _ = ssh.exec_command(f"cat {pass_file}")
    passwd = out.read().decode().strip()
    creds = credentials[username]
    if (len(creds) == 1):
        creds.append(passwd)
    else:
        creds[1] = passwd
    _, out, err = ssh.exec_command(
        f"nc localhost 30000 < {pass_file} | xargs | cut -d ' ' -f2")
    passwd = out.read().decode().strip()
    return username, passwd


@pwn
def bandit15():
    return r'openssl s_client -connect localhost:30001 -brief -ign_eof < /etc/bandit_pass/bandit15 2>&1 | tail -n 2 | xargs'


@save
def bandit16():
    username = "bandit16"
    connect(username)
    _, out, _ = ssh.exec_command('nmap -p 31000-32000 localhost')
    ports = re.findall(r'^\d{5}', out.read().decode().strip(), re.MULTILINE)
    for port in ports:
        _, out, _ = ssh.exec_command(
            F'cat /etc/bandit_pass/bandit16 | openssl s_client -connect localhost:{port} -quiet 2>/dev/null')
        response_header = out.readline()
        if "Correct" in response_header:
            rsa_key = out.read().decode()
            break

    return username, save_key(username, rsa_key)


@pwn
def bandit17():
    return r"diff passwords.new passwords.old  | grep '<' | cut -d ' ' -f2"


@pwn
def bandit18():
    return r"cat readme"


@pwn
def bandit19():
    return r"./bandit20-do cat /etc/bandit_pass/bandit20"


@save
def bandit20():
    username = "bandit20"
    connect(username)
    port = 4444
    _, out1, _ = ssh.exec_command(
        f'nc -lnvp {port} < /etc/bandit_pass/bandit20')
    client2 = paramiko.SSHClient()
    client2.load_system_host_keys()
    connect(username, client=client2)
    _ = client2.exec_command(f'./suconnect {port}')
    passwd = out1.read().decode().strip()
    client2.close()
    return username, passwd


@pwn
def bandit21():
    return r"cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv"


@pwn
def bandit22():
    return r"cat /tmp/8ca319486bfbbc3663ea0fbe81326349"


for i in range(31):
    try:
        eval(f"bandit{i}()")
    except Exception:
        break

# bandit13()
