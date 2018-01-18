from package1.module1 import module1_f1
from package1.module2 import module2_f1
from package1.subpackage2.submodule21 import submodule21_f1
from package1.subpackage3.swigpkg.myswig_module import myswig_module 


module1_f1('package1.main.py')
module2_f1('package1.main.py')
submodule21_f1('package1.main.py')

swig_m = myswig_module()
swig_m.print_myswig_module("package1.main.py")
