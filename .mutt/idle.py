#!/usr/bin/python
import imaplib
import os
import re
import select
import subprocess
import sys

IDLE_FOLDERS = [
    ("Ryan", "ryan@ryanpetrello.com", "INBOX", 'imap.fastmail.com'),
    ("Ryan", "ryan@ryanpetrello.com", "Sent", 'imap.fastmail.com'),

    ("RH", "rpetrell@redhat.com", "INBOX"),
]


def get_mail_pass(acct=None):
    acct = os.path.basename(acct)
    path = "/home/ryan/.passwd/%s.gpg" % acct
    args = ["gpg", "--use-agent", "--quiet", "--batch", "-d", path]
    try:
        return subprocess.check_output(args).strip()
    except subprocess.CalledProcessError:
        return ""


class _sock():

    def __init__(self, name, user, directory, server='imap.gmail.com'):
        password = get_mail_pass(user)
        self.name = name
        self.directory = directory
        print "Connecting to %s %s [%s]" % (name, user, server)
        self.imap = imaplib.IMAP4_SSL(server)
        self.imap.login(user, password)
        self.imap.select(self.directory)
        print "IDLE for %s" % self.directory
        self.imap.send("%s IDLE\r\n" % self.imap._new_tag())
        assert self.imap.readline() == '+ idling\r\n'

    def fileno(self):
        return self.imap.socket().fileno()


if __name__ == '__main__':
    sockets = [_sock(*args) for args in IDLE_FOLDERS]
    readable, _, _ = select.select(sockets, [], [], 60 * 5)  # 5 min timeout

    for sock in readable:
        print "-u basic -o"
        break


def prime_gpg_agent():
    ret = False
    i = 1
    while not ret:
        ret = (get_mail_pass("prime") == "prime")
        if i > 2:
            from offlineimap.ui import getglobalui
            sys.stderr.write("Error reading in passwords. Terminating.\n")
            getglobalui().terminate()
        i += 1
    return ret

prime_gpg_agent()
