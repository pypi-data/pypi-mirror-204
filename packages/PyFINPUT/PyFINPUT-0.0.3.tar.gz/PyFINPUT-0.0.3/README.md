# PyFINPUT
### Python File INPUT
At times, repeatedly using 20 command line arguments is frustrating.

Why not use an input file?

Import like this (I need to fix this...)

`pip install PyFINPUT==0.0.1`

`from PyFINPUT import pyfinput`

### 1. First, initiliase the input file class with the following arguments:

* `parser = pyfinput.input_file(...)`

* `filename: str` (required)
    
    The filename of the input file
* `case_sensitive: bool` (optional, def.: False)
 
    Whether the keywords are case sensitive of not
* `assigner: str` (optional, def.: "=")

    Character(s) to divide the keywords from their values: str
* `comment: str` (optional, def.: "#")
        
   Character(s) to identify the beginning of comment strings

### 2. Keywords can be added to the input_file object with the `add_keyword()` function:

* `name: str` (required)
   
   Name of keyword
* `kw_type: type` (optional, def.: str)
   
   Type of the keyword value(s)
* `nkws: int` (optional, def.: 1)
        
  Number of values in keyword, can also be "\*" or "+"
* `required: bool` (optional, def.: False)
  
  Raise an exception if True, but keyword not in file.
* `default: any` (optional, def.: "")
  
  The default value for the keyword


### 3. Finally, parse the file with the parse_file() function on the input_file object:
    returns:
        dict
        The returned dict contains the keywords as keys as strings,
        and their values as the dictionary values, with the defined
        type.