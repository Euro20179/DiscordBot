
import discord
from discord.ext import commands

class Content:
    def __init__(self, string, removeCmd=True):
        if removeCmd:
            split = string.split(" ")
            self.string = " ".join(split[1:])
            self.cmd = split[0]
        else: self.string = string
        self._i = -1
        self.ops_ = []
        self.opOps = []

    def calcOps(self):
        if not self.split(" ") or ("--" not in self and "—" not in self): return []
        for word in reversed(self.split(" ")):
            if "--" in word or "—" in word:
                self.ops_.append(word)
                foo = self.string
                self.replace(f' {word}', "")
                if foo == self.string:
                    self.replace(word, "")

    def split(self, splitBy, pastIndex=None, key=None):
        split = self.string.split(splitBy)
        if key:
            for n, s in enumerate(split):
                transformation = key(s)
                if transformation or not isinstance(transformation, bool):
                    split[n] = transformation
                else: 
                    if not transformation: split.pop(n)
        return split if not pastIndex else splitBy.join(split[pastIndex:])

    def replace(self, string, repWith, ret=False):
        if not ret: self.string = self.string.replace(string, repWith)
        else: return self.string.replace(string, repWith)
    
    def strip(self, other=None):
        return self.string.strip(other) if other else self.string.strip()

    def lower(self):
        return self.string.lower()
    
    def testOps(self, *ops):
        if not self.ops_: self.calcOps()
        for op in ops:
            if op in self.opOps or op in self.ops_:
                return True
        return False
    
    def ops(self):
        self.calcOps()
        for op in self.ops_:
            yield op

    def opsWithParams(self, paramcount : dict =None):
        """
        paramcount could be {'-param': arg_num}
        """
        l = self.split(" ")
        if not l[0]: return [(None, None)]
        for n, word in enumerate(l):
            if not word: continue
            if "-" == word[0] and word[1] != "-":
                if paramcount and word.strip("-") in paramcount.keys():
                    paramCount = paramcount.get(word.strip("-"))
                    if paramCount:
                        if isinstance(paramCount, tuple):
                            index = paramCount[0] if paramCount[0] else 1
                            splitBy = paramCount[1]
                            arg = " ".join(l[n + 1:]).split(splitBy)
                            self.opOps.append(word)
                            self.replace(f'{word} {splitBy.join(arg)}', "")
                            yield (word, arg[index].strip()) if not isinstance(index, slice) else (word, arg[index])
                        else:
                            self.opOps.append(word)
                            arg = l[l.index(word) + 1: l.index(word) + paramCount + 1]
                            self.replace(f'{word} {" ".join(arg)}', "")
                            yield (word, arg)
                else:
                    try:
                        self.opOps.append(word)
                        self.replace(f'{word} {"".join(l[l.index(word) + 1])}', "")
                        yield (word, "".join(l[l.index(word) + 1]))
                    except Exception as e:
                        print(e)
                        self.opOps.append(word)
                        self.replace(word, "")
                        yield(word, None)

    def getUser(self, msg, index=None, content=None):
        """
        index is the index where the user should be when content is split by spaces
        """
        if index:
            try: c = str(self.split(" ")[index].strip())
            except: return msg.author
        else:
            try: c = str(content)
            except: return msg.author
        c = c.replace("!", "")[2:-1] if "<@" in c else c
        if not c: c = str(msg.author.id)
        user = discord.utils.find(lambda m: str(m.id) == c or str(m.display_name.split("#")[0].lower()) == c.lower() or m.name.lower() == c.lower(), msg.guild.members)
        return user if user else msg.author

    def toSet(self, split=" ", pastIndex=None, key=None):
        """
        returns a set split by split
        """
        return set(self.split(" ", pastIndex=pastIndex, key=key))

    def suitibleForEval(self):
        return False if self.toSet() & {"help(", "quit()", "exit()", "os.", "token", "input(", "sys.", "__import__('os')", '__import__("os")',} else True
    
    def __len__(self):
        return len(self.string)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __add__(self, other):
        return self.string + other

    def __contains__(self, other):
        return other in self.string

    def __matmul__(self, other):
        if not self.ops_: self.calcOps()
        return other in self.ops_

    def __getitem__(self, other):
        if isinstance(other, slice):
            start, stop, step = other.indices(len(self))
            return self.string[start:stop:step]
        try:
            return self.string[other]
        except Exception as e: 
            print(e)
            return None

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._i += 1
        if self._i == len(self): 
            self._i = -1
            raise StopAsyncIteration
        return self.string[self._i]

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if self._i == len(self): 
            self._i = -1
            raise StopIteration
        return self.string[self._i]

    def __int__(self):
        return int(self.string)