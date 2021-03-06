# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.33
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _jaus.py
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class JAUSHeader(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, JAUSHeader, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, JAUSHeader, name)
    __repr__ = _swig_repr
    __swig_setmethods__["message_properties"] = _jaus.py.JAUSHeader_message_properties_set
    __swig_getmethods__["message_properties"] = _jaus.py.JAUSHeader_message_properties_get
    if _newclass:message_properties = _swig_property(_jaus.py.JAUSHeader_message_properties_get, _jaus.py.JAUSHeader_message_properties_set)
    __swig_setmethods__["command_code"] = _jaus.py.JAUSHeader_command_code_set
    __swig_getmethods__["command_code"] = _jaus.py.JAUSHeader_command_code_get
    if _newclass:command_code = _swig_property(_jaus.py.JAUSHeader_command_code_get, _jaus.py.JAUSHeader_command_code_set)
    __swig_setmethods__["dest_inst_id"] = _jaus.py.JAUSHeader_dest_inst_id_set
    __swig_getmethods__["dest_inst_id"] = _jaus.py.JAUSHeader_dest_inst_id_get
    if _newclass:dest_inst_id = _swig_property(_jaus.py.JAUSHeader_dest_inst_id_get, _jaus.py.JAUSHeader_dest_inst_id_set)
    __swig_setmethods__["dest_comp_id"] = _jaus.py.JAUSHeader_dest_comp_id_set
    __swig_getmethods__["dest_comp_id"] = _jaus.py.JAUSHeader_dest_comp_id_get
    if _newclass:dest_comp_id = _swig_property(_jaus.py.JAUSHeader_dest_comp_id_get, _jaus.py.JAUSHeader_dest_comp_id_set)
    __swig_setmethods__["dest_node_id"] = _jaus.py.JAUSHeader_dest_node_id_set
    __swig_getmethods__["dest_node_id"] = _jaus.py.JAUSHeader_dest_node_id_get
    if _newclass:dest_node_id = _swig_property(_jaus.py.JAUSHeader_dest_node_id_get, _jaus.py.JAUSHeader_dest_node_id_set)
    __swig_setmethods__["dest_subs_id"] = _jaus.py.JAUSHeader_dest_subs_id_set
    __swig_getmethods__["dest_subs_id"] = _jaus.py.JAUSHeader_dest_subs_id_get
    if _newclass:dest_subs_id = _swig_property(_jaus.py.JAUSHeader_dest_subs_id_get, _jaus.py.JAUSHeader_dest_subs_id_set)
    __swig_setmethods__["src_inst_id"] = _jaus.py.JAUSHeader_src_inst_id_set
    __swig_getmethods__["src_inst_id"] = _jaus.py.JAUSHeader_src_inst_id_get
    if _newclass:src_inst_id = _swig_property(_jaus.py.JAUSHeader_src_inst_id_get, _jaus.py.JAUSHeader_src_inst_id_set)
    __swig_setmethods__["src_comp_id"] = _jaus.py.JAUSHeader_src_comp_id_set
    __swig_getmethods__["src_comp_id"] = _jaus.py.JAUSHeader_src_comp_id_get
    if _newclass:src_comp_id = _swig_property(_jaus.py.JAUSHeader_src_comp_id_get, _jaus.py.JAUSHeader_src_comp_id_set)
    __swig_setmethods__["src_node_id"] = _jaus.py.JAUSHeader_src_node_id_set
    __swig_getmethods__["src_node_id"] = _jaus.py.JAUSHeader_src_node_id_get
    if _newclass:src_node_id = _swig_property(_jaus.py.JAUSHeader_src_node_id_get, _jaus.py.JAUSHeader_src_node_id_set)
    __swig_setmethods__["src_subs_id"] = _jaus.py.JAUSHeader_src_subs_id_set
    __swig_getmethods__["src_subs_id"] = _jaus.py.JAUSHeader_src_subs_id_get
    if _newclass:src_subs_id = _swig_property(_jaus.py.JAUSHeader_src_subs_id_get, _jaus.py.JAUSHeader_src_subs_id_set)
    __swig_setmethods__["data_ctrl"] = _jaus.py.JAUSHeader_data_ctrl_set
    __swig_getmethods__["data_ctrl"] = _jaus.py.JAUSHeader_data_ctrl_get
    if _newclass:data_ctrl = _swig_property(_jaus.py.JAUSHeader_data_ctrl_get, _jaus.py.JAUSHeader_data_ctrl_set)
    __swig_setmethods__["seq_num"] = _jaus.py.JAUSHeader_seq_num_set
    __swig_getmethods__["seq_num"] = _jaus.py.JAUSHeader_seq_num_get
    if _newclass:seq_num = _swig_property(_jaus.py.JAUSHeader_seq_num_get, _jaus.py.JAUSHeader_seq_num_set)
    def __init__(self, *args): 
        this = _jaus.py.new_JAUSHeader(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _jaus.py.delete_JAUSHeader
    __del__ = lambda self : None;
JAUSHeader_swigregister = _jaus.py.JAUSHeader_swigregister
JAUSHeader_swigregister(JAUSHeader)

class JAUSMessage(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, JAUSMessage, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, JAUSMessage, name)
    __repr__ = _swig_repr
    def setPriority(*args): return _jaus.py.JAUSMessage_setPriority(*args)
    def setACKNAK(*args): return _jaus.py.JAUSMessage_setACKNAK(*args)
    def __init__(self, *args): 
        this = _jaus.py.new_JAUSMessage(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _jaus.py.delete_JAUSMessage
    __del__ = lambda self : None;
JAUSMessage_swigregister = _jaus.py.JAUSMessage_swigregister
JAUSMessage_swigregister(JAUSMessage)

main = _jaus.py.main


