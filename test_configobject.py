from unittest import TestCase
from configobject import *

class test_ConfigObject(TestCase):        
    
    def test_subs(self):
    
        root = ConfigObject('root')
        root.sub('sub1')
        root.sub('sub2')
        root.sub1.sub('sub11')
        root.sub2.sub('sub21')
        
        root.value = 1
        root.sub1.value = 2
        root.sub2.value = 3
        root.sub1.sub11.value = 4
        root.sub2.sub21.value = 5
        
        resultdict = {
                      'value': 1,
                      'sub1.value': 2,
                      'sub2.value': 3,
                      'sub1.sub11.value': 4,
                      'sub2.sub21.value': 5
                      }
        
        valuedict = root.getValues()
        
        for key, value in resultdict.iteritems():
            self.assertEquals(valuedict[key], value)

class test_ConfigObjectParser(TestCase):        
    
    def test_parse(self):
        parser = ConfigObjectParser('testsuite/test_configobject.conf')
        configobject = parser.parse('test')
        resultdict = {
                      'numbers.int1' : 1,
                      'numbers.int2' : 2,
                      'numbers.float' : 1.1,
                      'numbers.pi' : 3.14,
                      'strings.string1' : "string1",
                      'strings.string2' : "string2",
                      'tuples.tuple1' : (1,2),
                      'tuples.tuple2' : (1,2.1),
                      'regexps.reg1' : "*\\.txt",
                      'regexps.reg2' : "(?P<jotain>\\w+)-(?P<jotain>\\w+)\\.picture"
                      }
        
        resultdict2 = {
                      'int1' : 1,
                      'int2' : 2,
                      'float' : 1.1,
                      'pi' : 3.14
                      }
        
        valuedict = configobject.getValues()
        valuedict2 = configobject.numbers.getValues()
                
        for key, value in resultdict.iteritems():
            self.assertEquals(valuedict[key], value)
        for key, value in resultdict2.iteritems():
            self.assertEquals(valuedict2[key], value)