# -*- coding: utf-8 -*-

from wox import Wox
import os
import re
import itertools
import subprocess


class PasswordStore(Wox):
    def indexed(self, pattern=None):
        path = os.path.join(os.environ['HOMEPATH'],
                            'password-store')
        t = []
        for _walk in os.scandir(path):
            if not _walk.name.startswith('.'):
                if _walk.is_file():
                    t.append(_walk.path)

                if _walk.is_dir():
                    dirs = [[os.path.join(i[0], t) for t in i[-1]]
                            for i in os.walk(_walk)]
                    single_list = itertools.chain(*dirs)
                    t.extend(single_list)

        return t

    def beautify_path(self, entry):
        title = entry.split('\\')[-1].split('.')[0].title()
        path = re.search(r"pass.*", entry)
        path = path.group(0)
        return [title, path]

    def query(self, query=None):
        results = []
        index_files = self.indexed()
        if not query:
            for i in range(6):
                title, path = self.beautify_path(index_files[i])
                results.append({
                    "Title": "{}".format(title),
                    "SubTitle": "{}".format(path),
                    "IcoPath": "Images/app.png"
                })
        else:
            for i in index_files:
                titles_gpg_files = i.split("\\")[-1]

                if not re.search(query, titles_gpg_files):
                    continue

                title, path = self.beautify_path(i)
                results.append({
                    "Title": "{}".format(title),
                    "SubTitle": "{}".format(path),
                    "IcoPath": "Images/app.png",
                    "JsonRPCAction": {
                        "method": "show",
                        "parameters": [i],
                        "dontHideAfterAction": False
                    }
                })

        return results

    def show(self, _f):
        command = "gpg --decrypt {}".format(os.path.join("C:", _f))
        with subprocess.Popen(command, stdout=subprocess.PIPE, shell=True) as proc:
            cmd_out = proc.stdout.read().split()[0]
            subprocess.run("echo {} | clip.exe".format(cmd_out.decode("utf-8")),
                           shell=True)

if __name__ == "__main__":
    PasswordStore()
