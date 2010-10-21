
from formatters import FormatterFactory

class ConfigObjectParser:
    
    def __init__(self, filename):
        self.file = filename
        self.formatterFactory = FormatterFactory()
    
    def _setsubvalue(self, configuration, configtree, value):
        if len(configtree) > 0:
            
            subconfig = configtree.pop(0)
            if not hasattr(configuration, subconfig):
                configuration.sub(subconfig)
                
            self._setsubvalue(getattr(configuration,subconfig), configtree, value)
        else:
            setattr(configuration, '_value', self.formatterFactory.getFormatted(value))

    def parse(self, name):
        
        configobject = ConfigObject(name)
        file = open(self.file, 'r')
        
        for line in file:
            line = line.split('#', 1)[0].strip()
            if line == '':
                continue
            configline, value = line.split('=')
            configtree = configline.strip().split('.')
            self._setsubvalue(configobject, configtree, value.strip())

        return configobject

class ConfigObject:
    
    def __init__(self, name):
        self._name = name
        
    def sub(self, name):
        setattr(self, name, ConfigObject(name))
        
    def getValues(self, super=None):
        selfvaluedict   = self.__dict__
        valuedict = dict()
        if super == None:
            fullname = ''
        else:
            fullname = super + self._name + '.'
        for key, value in selfvaluedict.iteritems():
            if key == '_name':
                continue
            elif isinstance(value, ConfigObject):
                valuedict.update(value.getValues(fullname))
            elif key ==  '_value' and fullname != '':
                valuedict[fullname[0:-1]] = value
            else:
                valuedict[fullname + key] = value
        return valuedict
    
    def getSubs(self):
        
        selfvaluedict   = self.__dict__
        subdict = dict()
        for key, value in selfvaluedict.iteritems():
            if isinstance(value, ConfigObject):
                subdict[key] = value
        return subdict