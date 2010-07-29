# -*- coding: utf-8 -*-

from __future__ import with_statement
from pprint import pprint
from os.path import exists
from os.path import join
from shutil import copy


########################################################################
class ConfigParser:
    """
    holds and manage the configuration
    
    current dict layout:
    
    {
    
     section : { 
      option : { 
            value:
            type:
            desc:
      }
      desc: 
    
    }
    
    
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.config = {} # the config values
        self.plugin = {} # the config for plugins
        
        self.username = ""
        self.password = ""
        #stored outside and may not modified
        
        #@TODO start setup..
        
        self.checkVersion()
        
        self.readConfig()
    
    #----------------------------------------------------------------------
    def checkVersion(self):
        """determines if config need to be copied"""
        
        if not exists("pyload.config"):
            copy(join(pypath,"module", "config", "default.config"), "pyload.config")
            
        if not exists("plugin.config"):
            f = open("plugin.config", "wb")
            f.close()
        
        #@TODO: testing conf file version
        
    #----------------------------------------------------------------------
    def readConfig(self):
        """reads the config file"""
        
        self.config = self.parseConfig(join(pypath,"module", "config", "default.config"))
        self.plugin = self.parseConfig("plugin.config")
        
        try:
            homeconf = self.parseConfig("pyload.config")
            self.updateValues(homeconf, self.config)
            
        except Exception, e:
            print e
        
            
        self.username = self.config["remote"]["username"]["value"]
        del self.config["remote"]["username"]
        
        self.password = self.config["remote"]["password"]["value"]
        del self.config["remote"]["password"]
        
        
    #----------------------------------------------------------------------
    def parseConfig(self, config):
        """parses a given configfile"""
        
        f = open(config)
        
        config = f.read()

        config = config.split("\n")
        
        conf = {}
        
        section, option, value, typ, desc = "","","","",""
        
        listmode = False
        
        for line in config:
            
            line = line.rpartition("#") # removes comments
            
            if line[1]:
                line = line[0]
            else:
                line = line[2]
            
            line = line.strip()            
            
            try:
            
                if line == "":
                    continue
                elif line.endswith(":"):
                    section, none, desc = line[:-1].partition('-')
                    section = section.strip()
                    desc = desc.replace('"', "").strip()
                    conf[section] = { "desc" : desc }
                else:
                    if listmode:
                        
                        if line.endswith("]"):
                            listmode = False
                            line = line.replace("]","")
                            
                        value += [self.cast(typ, x.strip()) for x in line.split(",") if x]
                        
                        if not listmode:
                            conf[section][option] = { "desc" : desc,
                                                      "typ" : typ,
                                                      "value" : value} 
                        
                        
                    else:
                        content, none, value = line.partition("=")
                        
                        content, none, desc = content.partition(":")
                        
                        desc = desc.replace('"', "").strip()
    
                        typ, option = content.split()
                        
                        value = value.strip()
                        
                        if value.startswith("["):
                            if value.endswith("]"):                            
                                listmode = False
                                value = value[:-1]
                            else:
                                listmode = True
                          
                            value = [self.cast(typ, x.strip()) for x in value[1:].split(",") if x]
                        else:
                            value = self.cast(typ, value)
                        
                        if not listmode:
                            conf[section][option] = { "desc" : desc,
                                                      "typ" : typ,
                                                      "value" : value}
                
            except:
                pass
                    
                        
        f.close()
        return conf
        
    
    
    #----------------------------------------------------------------------
    def updateValues(self, config, dest):
        """sets the config values from a parsed config file to values in destination"""
                                
        for section in config.iterkeys():
    
            if dest.has_key(section):
                
                for option in config[section].iterkeys():
                    
                    if option == "desc": continue
                    
                    if dest[section].has_key(option):
                        dest[section][option]["value"] = config[section][option]["value"]
                        
                    else:
                        dest[section][option] = config[section][option]
                
                
            else:
                dest[section] = config[section]

    #----------------------------------------------------------------------
    def saveConfig(self, config, filename):
        """saves config to filename"""
        #@TODO save username and config
        with open(filename, "wb") as f:
           
            for section in config.iterkeys():
                f.write('%s - "%s":\n' % (section, config[section]["desc"]))
                
                for option, data in config[section].iteritems():
                    
                    if option == "desc": continue
                    
                    if isinstance(data["value"], list):
                        value = "[ \n"
                        for x in data["value"]:
                            value += "\t\t" + x + ",\n"
                        value += "\t\t]\n"
                    else:
                        value = data["value"] + "\n"
                    
                    f.write('\t%s %s : "%s" = %s' % (data["typ"], option, data["desc"], value) )
    #----------------------------------------------------------------------
    def cast(self, typ, value):
        """cast value to given format"""
        if typ == "int":
            return int(value)
        elif typ == "bool":
            return True if value.lower() in ("true", "on", "an","yes") else False
        else:
            return value
                
    #----------------------------------------------------------------------
    def save(self):
        """saves the configs to disk"""
        self.saveConfig(self.config, "pyload.config")
        self.saveConfig(self.plugin, "plugin.config")
        
    #----------------------------------------------------------------------
    def __getitem__(self, section):
        """provides dictonary like access: c['section']['option']"""
        return Section(self, section)
    
    #----------------------------------------------------------------------
    def get(self, section, option):
        """get value"""
        return self.config[section][option]["value"]
        
    #----------------------------------------------------------------------
    def set(self, section, option, value):
        """set value"""
        self.config[section][option]["value"] = value
        
    #----------------------------------------------------------------------
    def getPlugin(self, plugin, option):
        """gets a value for a plugin"""
        return self.plugin[plugin][option]["value"]
    
    #----------------------------------------------------------------------
    def setPlugin(self, plugin, option, value):
        """sets a value for a plugin"""
        self.plugin[plugin][option]["value"] = value
        

########################################################################
class Section:
    """provides dictionary like access for configparser"""

    #----------------------------------------------------------------------
    def __init__(self, parser, section):
        """Constructor"""
        self.parser = parser
        self.section = section
        
    #----------------------------------------------------------------------
    def __getitem__(self, item):
        """getitem"""
        return self.parser.get(self.section, item)
        
    #----------------------------------------------------------------------
    def __setitem__(self, item, value):
        """setitem"""
        self.parser.set(self.section, item, value)
    
        
    
if __name__ == "__main__":
    pypath = ""

    from time import time,sleep
    
    a = time()
    
    c = ConfigParser()
    
    b = time()
    
    print "sec", b-a    
    
    pprint(c.config)
    
    c.saveConfig(c.config, "user.conf")