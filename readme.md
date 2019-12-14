Usage:
```                    
usage: pastes.py [-h] [-n NAME] [-t TAG]
                 [-l {bash,c++,c#,css,diff,java,javascript,perl,php,plain,python,ruby,sql,xml}]
                 file [file ...]

positional arguments:
  file                  Put either a file, or rawtext

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name of the paste
  -t TAG, --tag TAG     Tag description of paste
  -l --language {bash,c++,c#,css,diff,java,javascript,perl,php,plain,python,ruby,sql,xml}    Programming language


                    ```
                    Example:
                    ```
pastes.py -l php -n "Pasteros API controller" controllers/Api_Controller.php

pastes.py --language c++ --tag myCurrentCPlusPlusProject "#include <iostream> int main(){std::cout << 1 << std::endl;}"
                    ```
                    The client will return the link to the pastes as well as the delete URL
                    
       