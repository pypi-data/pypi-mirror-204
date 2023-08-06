"""
PyFINPUT
Benedict Saunders (c) 2023
Licensed under the GNU General Public License v3.0


Module for adding a simple input file. It's in the style of argparse:

First, initiliase the input file class with the following arguments:

    filename: str (required)
        The filename of the input file
    case_sensitive: bool (optional, def.: False)
        Whether the keywords are case sensitive of not
    assigner: str (optional, def.: "=")
        Character(s) to divide the keywords from their
        values: str
    comment: str (optional, def.: "#")
        Character(s) to identify the beginning of
        comment strings

Keywords can be added to the input_file object with the "add_keyword()"
function:

    name: str (required)
        Name of keyword
    kw_type: type (optional, def.: str)
        Type of the keyword value(s)
    nkws: int (optional, def.: 0)
        Number of values in keyword
        Can also be "*" or "+"
    required: bool (optional, def.: False)
        Raise an exception if True, but
        keyword not in file.
    default: any (optional, def.: "")
        The default value for the keyword

Similarly, blocks can be defined with the "add_block()" function.
The input is identical to that of a keyword, but with the addtion of
two more arguments:
    nperline: int (optional, def.: 1)
        Number of items per line
    minlines: int (optional, def.: 0)
        minimum number of lines to expect in the block

Finally, parse the file with the parse_file() function on the input_file
object:
    returns:
        dict
        The returned dict contains the keywords as keys as strings,
        and their values as the dictionary values, with the defined
        type.

Note: the package handles some string manipulation with shlex, and
therefor strings can be grouped with double quotes, for example, the
following will be treated as 4 values:

>> "A string" something else "and another" <<

"""

import shlex
from utils import *

class keyword:
    def __init__(self,        
        name = None,
        kw_type = any,
        nkws = 1,
        req = False,
        default = None) -> None:
        self.name = name,
        self.type = kw_type,
        self.nkws = nkws
        self.required = req
        self.handled = False
        self.default = default

class block(keyword):
    def __init__(self, name=None, kw_type=any, minlines=1, nperline: int = 1, req=False, default=None) -> None:
        super().__init__(name, kw_type, minlines, req, default)
        self.minlines = minlines
        self.nperline = nperline

class input_file:
    def __init__(self, name: str, case_sensitive: bool = False, assigner: str = ":", comment: str = "#", blocker = "%", endblock = "end_") -> None:
        self.filename = name
        self.kws = []
        self.blocks = []
        self.cs = case_sensitive
        self.assigner = assigner
        self.cmt_id = comment
        self.blocker = blocker
        self.endblock = endblock

    def _set_type(self, v, t):
        if not isinstance(v, list):
            v = [v]
        if t == str:
            v = [a.strip('\"') for a in v]
        elif t == bool:
            v = [0 if a.casefold() in ["0".casefold(), "F".casefold(), "FALSE".casefold()] else 1 for a in v]
        if len(v) == 1:
            v = v[0]
        return v

    def add_keyword(
        self,
        name: str,
        kw_type = str,
        default = None,
        nkws: int = 0,
        required: bool = False,
    ) -> None:
        self.kws.append(keyword(name, kw_type=kw_type, nkws=nkws, req=required, default=default))

    def add_block(
        self,
        name: str,
        type: type,
        default: any = [None],
        minlines: int = 1,
        nperline: int = 0,
        required: bool = False
        ) -> None:
        self.blocks.append(block(name, kw_type=type, minlines=minlines, nperline = nperline, req=required, default=default))


    def parse_file(self) -> dict:
        with open(self.filename, "r") as f:
            # First we need to remove comments
            lines = [l.strip() for l in f.readlines() if not l.strip().startswith(self.cmt_id)]
            lines = [l.split(self.cmt_id)[0] for l in lines]

        # Set params dict to contain defaults
        params = dict([(kw.name[0], kw.default) for kw in self.kws if kw.required == False] + [(b.name[0], b.default) for b in self.blocks if b.required == False])
        unhandled_kws = [keyword.name[0] for keyword in self.kws]
        unhandled_blocks = [block.name[0] for block in self.blocks]
        required = [keyword.name[0] for keyword in self.kws if any([keyword.required == True, keyword.nkws == "+"])] + [block.name[0] for block in self.blocks]
        in_block = False
        current = None
        current_block_list = []

        # Iterate through the lines witout comments
        for idx, line in enumerate(lines):
            if line == "":
                continue
            
            #############################
            # BLOCK HANDLING ############
            #############################
            if line.startswith(self.blocker) or in_block:

                # Clsoing the block, and adding to the parameters dictionary

                if in_block and f"{self.blocker}{self.endblock}{self.blocks[bidx].name[0]}" in line:
                    if len(current_block_list) < current.minlines:
                        raise LookupError(f"Found fewer memebers of block {current.name} than requested. Expected {current.minlines} but found {len(current_block_list)}")
                    params[current.name[0]] = current_block_list
                    in_block = False
                    unhandled_blocks.remove(current.name[0])
                    if current.name[0]:
                        required.remove(current.name[0])
                    current = None
                    current_block_list = []
                    continue
                
                # If the block is open, but no block identifier found, add the data to the block list.

                elif in_block:
                    line = shlex.split(line.strip())
                    if current.nperline == 0:
                        current.nperline = len(line)
                    if len(line) > current.nperline:
                        raise IndexError(f"\n\tToo many items on line of {current.name[0]}. Expected {current.nperline}, found {len(line)}")
                    else:
                        if len(line) == 1:
                            line = line[0]
                        current_block_list.append(line)
                    continue

                # Open a new block

                else:
                    if self.blocker in line and f"{self.blocker}{self.endblock}" not in line:
                        block_name = line.split(self.blocker)[1]
                        bidx = [b.name[0] for b in self.blocks].index(block_name)
                        current = self.blocks[bidx]
                        in_block = True
            
            elif in_block and self.blocker in line and self.endblock not in line:
                raise LookupError(f"Block identifier found without closing statement while in block {self.current_block}")

            else:
                assert in_block == False

            ###############################
            # KEYWORD HANDLING ############
            ###############################
                k, v = [l.strip() for l in line.split(self.assigner)]
                for kw in self.kws:
                    if kw.name[0] == k and k in unhandled_kws:
                        if k in required:
                            required.remove(k)
                        unhandled_kws.remove(k)

                        # Doing stuff with keywords of multiple members
                        if kw.nkws in ["*", "+", 0]:
                            v = shlex.split(v)
                            kw.nkws = len(v)
                        elif kw.nkws == 1:
                            if len(shlex.split(v)) > 1:
                                raise LookupError(f"\n\tToo many members for keyword: {k}\n\t{len(shlex.split(v))} found, but {kw.nkws} expected")
                        elif kw.nkws > 1:
                            v = shlex.split(v)
                            if len(v) != kw.nkws:
                                raise LookupError(f"\n\tIllegal number of members for keyword: {k}\n\t{len(v)} found, but {kw.nkws} expected")                                    
                        v = self._set_type(v, kw.type[0])
                        params[k] = v
                        break
                    else:
                        pass
                        #raise LookupError(f"\n\tMultiple occurences of keyword {k} ")
                
        # If a keyword is set as required, make sure it is actually provided.
        if len(required) > 0:
            print("\tMissing required keyword(s):")
            _ = [print(f"\n\t{mkw}") for mkw in required]
            exit()
        return params     
