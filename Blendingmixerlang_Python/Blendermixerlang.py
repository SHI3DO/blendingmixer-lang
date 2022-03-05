import os
import re
import hashlib
import subprocess


class Blendermixerlang:
    def __init__(self):
        super().__init__()

    def read(self, blemixf):
        blemixfile = open(blemixf, 'r', encoding='UTF-8')
        content = blemixfile.read()
        blemixfile.close()
        compiled = self.parse(content.replace(' ', '').replace('\n', ''))
        compiled = '\n'.join(compiled)

        outf = open(str(blemixf).replace('blemix', 'py'), 'w', encoding='UTF-8')
        outf.write(compiled)
        outf.close()

        subprocess.call(['python', str(blemixf).replace('blemix', 'py')])
        os.remove(str(blemixf).replace('blemix', 'py'))

    def parse(self, content):
        compiled = ''
        compiled = self.ruleset(self.parse_find(content))
        return compiled

    def parse_find(self, content):
        tmp = []
        for n in range(0, content.count('믹서기')):
            tmp.append(content[0:content.find('믹서기') + 3])
            content = content.replace(content[0:content.find('믹서기') + 3], '')
            self.parse_find(content)
        return tmp

    def ruleset(self, content):
        compiled = []
        for i in content:
            if str(i).count('진공') > 0:
                var = re.search('진공(.+?)~', str(i)).group(1)
                value = re.search('~(.+?)믹서기', str(i)).group(1)
                contentvalue = self.declare_var(var, value)
                compiled.append(contentvalue)

            if str(i).count('초고속') > 0:
                value = re.search('초고속(.+?)믹서기', str(i)).group(1)
                contentvalue = self.print_func(value)
                compiled.append(contentvalue)

        return compiled

    def declare_var(self, var, value):
        tmpvalue = 0
        cu = value.count('쿠')
        bbing = value.count('삥')
        tmpvalue = tmpvalue + cu
        tmpvalue = tmpvalue - bbing

        tmpvar = self.hashconvert(hashlib.sha256(var.encode()).hexdigest())

        return f'{tmpvar} = {tmpvalue}'

    def print_func(self, value):
        return f'print({self.hashconvert(hashlib.sha256(value.encode()).hexdigest())})'

    def hashconvert(self, string):
        string = str(string).replace('0', 'a')
        string = str(string).replace('1', 'b')
        string = str(string).replace('2', 'c')
        string = str(string).replace('3', 'd')
        string = str(string).replace('4', 'e')
        string = str(string).replace('5', 'f')
        string = str(string).replace('6', 'g')
        string = str(string).replace('7', 'h')
        string = str(string).replace('8', 'i')
        string = str(string).replace('9', 'j')

        return string
