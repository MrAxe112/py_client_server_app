import subprocess


def new_ping(site):
    args = ['ping', site]
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))


new_ping('yandex.ru')
new_ping('youtube.com')
