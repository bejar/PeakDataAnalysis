#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tools import *
from suffix_array import Suffix_array


path = './test'
str = 'aabbbaaabbba'
str_unicode = utf82unicode(str)
sa1 = Suffix_array()
sa1._add_str(str_unicode)
sa1._add_str(str_unicode)
sa1.karkkainen_sort()
# print sa1.equiv
#print "["+sa1.fusion+"]"
#print sa1.path_array
#print sa1.str_array
#print sa1.suffix_array
#sa1._verif_suffix_array()
sa1._write_su_n(5)
 
  
  
  
  
  
