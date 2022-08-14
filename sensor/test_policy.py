import subprocess


def test_policy(rule):
    cmd1 = f"snort -c /usr/lcoal/snort/etc/snort.lua -R {rule}"
    res = subprocess.Popen(cmd1, shell=True)
    return res.poll()
