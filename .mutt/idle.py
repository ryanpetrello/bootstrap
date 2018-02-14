#!/usr/bin/python
import imaplib
import hashlib
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


def get_mail_pass(acct):
    acct = os.path.basename(hashlib.md5(acct).hexdigest())
    path = "/home/ryan/.passwd/%s" % acct
    args = ["ansible-vault", "decrypt", path, "--vault-password-file",
            "/home/ryan/.v", "--output", "-"]
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
