"""
Utilities for parsing torchscipt IR graphs
"""

def parse_attributes(node):
    # This assumes that the name and attribute are in the
    # last [..] pattern occurence: might break?
    segment = str(node).split('[')[-1].split(']')[0]
    items = segment.split('=')
    attributes = {}
    for k, v in zip(items[::2], items[1::2]):
        v = v.strip('"')
        attributes[k] = v
    return attributes

def get_attr_name(node):
    return parse_attributes(node)['name']

def get_type(x):
    return x.type().str()

def get_input_names(node):
    return [x.debugName() for x in node.inputs()]

def get_tensorial_input_names(node):
    return [x.debugName() for x in node.inputs() if istensor(x) or istensorlist(x)]

def get_output_names(node):
    return [x.debugName() for x in node.outputs()]

def get_inputs_outputs_sourceref(node, tensorial_inputs=False):
    if tensorial_inputs:
        inputs = get_tensorial_input_names(node)
    else:
        inputs = get_input_names(node)
    outputs = get_output_names(node)
    sourceref = node.sourceRange()
    return inputs, outputs, sourceref

def istensor(x):
    return get_type(x) == 'Tensor'

def istensorlist(x):
    return get_type(x) == 'Tensor[]'

def ismodule(x):
    return get_type(x).startswith('__torch__')

_CASTERS = {'int': int, 'float': float, 'bool': lambda x: bool(int(x))}
def get_value(x, module=None):
    typ_str = get_type(x)
    if typ_str in _CASTERS:
        attrs = parse_attributes(x.node())
        if x.node().kind() == 'prim::GetAttr':
            return get_attribute_value(x, module)
        else:
            value = attrs['value']
            v = _CASTERS[typ_str](value)
            return v
    else:
        return None

def get_attribute_value(x, module):
    assert module is not None
    attrs = parse_attributes(x.node())
    value = getattr(module, attrs['name'])
    return value

def get_list(x, module=None):
    node = x.node()
    return [get_value(xx, module=module) for xx in node.inputs()]

def isaten(node):
    return node.kind().startswith('aten::')

def hasaten(graph):
    if graph is None:
        return False
    return any([isaten(node) for node in graph.nodes()])

def isgetparam(node):
    return node.kind() == 'prim::GetAttr' and istensor(node.output())

def isgetattr(node):
    return node.kind() == 'prim::GetAttr' and not istensor(node.output())

def isgetattrmodule(node):
    return isgetattr(node) and ismodule(node.output())

def iscallmethod(node):
    return node.kind() == 'prim::CallMethod'

def isprimcallmethod(node):
    return node.kind() == 'prim::PythonOp' and node.pyname() == 'forward'

def islistconstruct(node, tensorlist=True):
    result = node.kind() == 'prim::ListConstruct'
    if result and tensorlist:
        result = istensorlist(node.output())
    return result

def islistunpack(node):
    return node.kind() == 'prim::ListUnpack'

def istupleconstruct(node):
    return node.kind() == 'prim::TupleConstruct'

def istupleunpack(node):
    return node.kind() == 'prim::TupleUnpack'

def isprint(node):
    return node.kind() == 'prim::Print'

def hasgetparam(graph):
    if graph is None:
        return False
    return any([isgetparam(node) for node in graph.nodes()])

def get_function_name(node):
    assert node.kind() == 'prim::CallFunction'
    return next(node.inputs()).type().__repr__()

def isfunctional(node):
    if node.kind() == 'prim::CallFunction':
        funcname = get_function_name(node)
        return funcname.startswith('__torch__.torch.nn.functional.')
    else:
        return False

def isuserfunction(node):
    if node.kind() == 'prim::CallFunction':
        funcname = get_function_name(node)
        return not funcname.startswith('__torch__.torch.nn.functional.')
    else:
        return False

def isNone(node):
    if (node.kind() == 'prim::Constant') and (str(node).find('None') != -1):
        return True
    else:
        return False

def getfunctionalname(node):
    assert isfunctional(node)
    funcname = get_function_name(node)
    assert funcname.startswith('__torch__')
    funcname = funcname.split('__torch__.')[1]
    assert funcname.startswith('torch.nn.functional'), (
        'User defined functions are not supported. Function: {}'.format(funcname))
    funcname = 'F.' + funcname.split('torch.nn.functional.')[1]
    return funcname

def getuserfuncname(node):
    assert isuserfunction(node)
    funcname = get_function_name(node)
    assert funcname.startswith('__torch__')
    funcname = funcname.split('__torch__.')[1]
    return funcname

def hasfunctional(graph):
    return any([isfunctional(node) for node in graph.nodes()])

def hasuserfunction(graph):
    return any([isuserfunction(node) for node in graph.nodes()])

def needspatching(graph):
    if graph is None:
        raise ValueError('Could not get graph')
    else:
        return any([hasgetparam(graph), hasaten(graph), hasfunctional(graph), hasuserfunction(graph)])
