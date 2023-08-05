
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _esi_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "esi"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CapnpDecodeOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.decode.capnp"

  _ODS_REGIONS = (0, True)

  def __init__(self, decodedData, clk, valid, capnpBits, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clk))
    operands.append(_get_op_result_or_value(valid))
    operands.append(_get_op_result_or_value(capnpBits))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(decodedData)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clk(self):
    return self.operation.operands[0]

  @builtins.property
  def valid(self):
    return self.operation.operands[1]

  @builtins.property
  def capnpBits(self):
    return self.operation.operands[2]

  @builtins.property
  def decodedData(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CapnpEncodeOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.encode.capnp"

  _ODS_REGIONS = (0, True)

  def __init__(self, capnpBits, clk, valid, dataToEncode, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clk))
    operands.append(_get_op_result_or_value(valid))
    operands.append(_get_op_result_or_value(dataToEncode))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(capnpBits)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clk(self):
    return self.operation.operands[0]

  @builtins.property
  def valid(self):
    return self.operation.operands[1]

  @builtins.property
  def dataToEncode(self):
    return self.operation.operands[2]

  @builtins.property
  def capnpBits(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ChannelBufferOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.buffer"

  _ODS_REGIONS = (0, True)

  def __init__(self, output, clk, rst, input, *, stages=None, name=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clk))
    operands.append(_get_op_result_or_value(rst))
    operands.append(_get_op_result_or_value(input))
    _ods_context = _ods_get_default_loc_context(loc)
    if stages is not None: attributes["stages"] = (stages if (
        issubclass(type(stages), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('I64Attr')) else
          _ods_ir.AttrBuilder.get('I64Attr')(stages, context=_ods_context))
    if name is not None: attributes["name"] = (name if (
        issubclass(type(name), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('StrAttr')) else
          _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    results.append(output)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clk(self):
    return self.operation.operands[0]

  @builtins.property
  def rst(self):
    return self.operation.operands[1]

  @builtins.property
  def input(self):
    return self.operation.operands[2]

  @builtins.property
  def stages(self):
    if "stages" not in self.operation.attributes:
      return None
    return _ods_ir.IntegerAttr(self.operation.attributes["stages"])

  @stages.setter
  def stages(self, value):
    if value is not None:
      self.operation.attributes["stages"] = value
    elif "stages" in self.operation.attributes:
      del self.operation.attributes["stages"]

  @stages.deleter
  def stages(self):
    del self.operation.attributes["stages"]

  @builtins.property
  def name(self):
    if "name" not in self.operation.attributes:
      return None
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is not None:
      self.operation.attributes["name"] = value
    elif "name" in self.operation.attributes:
      del self.operation.attributes["name"]

  @name.deleter
  def name(self):
    del self.operation.attributes["name"]

  @builtins.property
  def output(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CosimEndpointOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.cosim"

  _ODS_REGIONS = (0, True)

  def __init__(self, recv, clk, rst, send, name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clk))
    operands.append(_get_op_result_or_value(rst))
    operands.append(_get_op_result_or_value(send))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    issubclass(type(name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    results.append(recv)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clk(self):
    return self.operation.operands[0]

  @builtins.property
  def rst(self):
    return self.operation.operands[1]

  @builtins.property
  def send(self):
    return self.operation.operands[2]

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def recv(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CustomServiceDeclOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.decl"

  _ODS_REGIONS = (1, True)

  def __init__(self, sym_name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    issubclass(type(sym_name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def ports(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ESIPureModuleInputOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.pure_module.input"

  _ODS_REGIONS = (0, True)

  def __init__(self, value, name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    issubclass(type(name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    results.append(value)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

  @builtins.property
  def value(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ESIPureModuleOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.pure_module"

  _ODS_REGIONS = (1, True)

  def __init__(self, sym_name, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    issubclass(type(sym_name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def body(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ESIPureModuleOutputOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.pure_module.output"

  _ODS_REGIONS = (0, True)

  def __init__(self, name, value, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(value))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    issubclass(type(name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def value(self):
    return self.operation.operands[0]

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ESIPureModuleParamOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.pure_module.param"

  _ODS_REGIONS = (0, True)

  def __init__(self, name, type_, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["name"] = (name if (
    issubclass(type(name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(name, context=_ods_context))
    attributes["type"] = (type_ if (
    issubclass(type(type_), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(type_, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def name(self):
    return _ods_ir.StringAttr(self.operation.attributes["name"])

  @name.setter
  def name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["name"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class NullSourceOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.null"

  _ODS_REGIONS = (0, True)

  def __init__(self, out, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(out)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def out(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PipelineStageOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.stage"

  _ODS_REGIONS = (0, True)

  def __init__(self, output, clk, rst, input, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(clk))
    operands.append(_get_op_result_or_value(rst))
    operands.append(_get_op_result_or_value(input))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(output)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def clk(self):
    return self.operation.operands[0]

  @builtins.property
  def rst(self):
    return self.operation.operands[1]

  @builtins.property
  def input(self):
    return self.operation.operands[2]

  @builtins.property
  def output(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class RandomAccessMemoryDeclOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.mem.ram"

  _ODS_REGIONS = (0, True)

  def __init__(self, sym_name, innerType, depth, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["sym_name"] = (sym_name if (
    issubclass(type(sym_name), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(sym_name, context=_ods_context))
    attributes["innerType"] = (innerType if (
    issubclass(type(innerType), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(innerType, context=_ods_context))
    attributes["depth"] = (depth if (
    issubclass(type(depth), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('I64Attr')) else
      _ods_ir.AttrBuilder.get('I64Attr')(depth, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def sym_name(self):
    return _ods_ir.StringAttr(self.operation.attributes["sym_name"])

  @sym_name.setter
  def sym_name(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["sym_name"] = value

  @builtins.property
  def depth(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["depth"])

  @depth.setter
  def depth(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["depth"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class RequestInOutChannelOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.req.inout"

  _ODS_REGIONS = (0, True)

  def __init__(self, toClient, servicePort, toServer, clientNamePath, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(toServer))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["servicePort"] = (servicePort if (
    issubclass(type(servicePort), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('HWInnerRefAttr')) else
      _ods_ir.AttrBuilder.get('HWInnerRefAttr')(servicePort, context=_ods_context))
    attributes["clientNamePath"] = (clientNamePath if (
    issubclass(type(clientNamePath), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
      _ods_ir.AttrBuilder.get('StrArrayAttr')(clientNamePath, context=_ods_context))
    results.append(toClient)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def toServer(self):
    return self.operation.operands[0]

  @builtins.property
  def toClient(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class RequestToClientConnectionOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.req.to_client"

  _ODS_REGIONS = (0, True)

  def __init__(self, toClient, servicePort, clientNamePath, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["servicePort"] = (servicePort if (
    issubclass(type(servicePort), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('HWInnerRefAttr')) else
      _ods_ir.AttrBuilder.get('HWInnerRefAttr')(servicePort, context=_ods_context))
    attributes["clientNamePath"] = (clientNamePath if (
    issubclass(type(clientNamePath), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
      _ods_ir.AttrBuilder.get('StrArrayAttr')(clientNamePath, context=_ods_context))
    results.append(toClient)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def toClient(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class RequestToServerConnectionOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.req.to_server"

  _ODS_REGIONS = (0, True)

  def __init__(self, servicePort, toServer, clientNamePath, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(toServer))
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["servicePort"] = (servicePort if (
    issubclass(type(servicePort), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('HWInnerRefAttr')) else
      _ods_ir.AttrBuilder.get('HWInnerRefAttr')(servicePort, context=_ods_context))
    attributes["clientNamePath"] = (clientNamePath if (
    issubclass(type(clientNamePath), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrArrayAttr')) else
      _ods_ir.AttrBuilder.get('StrArrayAttr')(clientNamePath, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def toServer(self):
    return self.operation.operands[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ServiceDeclInOutOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.inout"

  _ODS_REGIONS = (0, True)

  def __init__(self, inner_sym, toServerType, toClientType, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["inner_sym"] = (inner_sym if (
    issubclass(type(inner_sym), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(inner_sym, context=_ods_context))
    attributes["toServerType"] = (toServerType if (
    issubclass(type(toServerType), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(toServerType, context=_ods_context))
    attributes["toClientType"] = (toClientType if (
    issubclass(type(toClientType), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(toClientType, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inner_sym(self):
    return _ods_ir.StringAttr(self.operation.attributes["inner_sym"])

  @inner_sym.setter
  def inner_sym(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["inner_sym"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ServiceHierarchyMetadataOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.hierarchy.metadata"

  _ODS_REGIONS = (0, True)

  def __init__(self, serverNamePath, impl_type, clients, *, service_symbol=None, impl_details=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    if service_symbol is not None: attributes["service_symbol"] = (service_symbol if (
        issubclass(type(service_symbol), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
          _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(service_symbol, context=_ods_context))
    attributes["serverNamePath"] = (serverNamePath if (
    issubclass(type(serverNamePath), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('ArrayAttr')) else
      _ods_ir.AttrBuilder.get('ArrayAttr')(serverNamePath, context=_ods_context))
    attributes["impl_type"] = (impl_type if (
    issubclass(type(impl_type), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(impl_type, context=_ods_context))
    if impl_details is not None: attributes["impl_details"] = (impl_details if (
        issubclass(type(impl_details), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('DictionaryAttr')) else
          _ods_ir.AttrBuilder.get('DictionaryAttr')(impl_details, context=_ods_context))
    attributes["clients"] = (clients if (
    issubclass(type(clients), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('ArrayAttr')) else
      _ods_ir.AttrBuilder.get('ArrayAttr')(clients, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def impl_type(self):
    return _ods_ir.StringAttr(self.operation.attributes["impl_type"])

  @impl_type.setter
  def impl_type(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["impl_type"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ServiceImplementReqOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.impl_req"

  _ODS_REGIONS = (1, True)

  def __init__(self, outputs, impl_type, inputs, *, service_symbol=None, impl_opts=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    _ods_context = _ods_get_default_loc_context(loc)
    if service_symbol is not None: attributes["service_symbol"] = (service_symbol if (
        issubclass(type(service_symbol), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
          _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(service_symbol, context=_ods_context))
    attributes["impl_type"] = (impl_type if (
    issubclass(type(impl_type), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(impl_type, context=_ods_context))
    if impl_opts is not None: attributes["impl_opts"] = (impl_opts if (
        issubclass(type(impl_opts), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('DictionaryAttr')) else
          _ods_ir.AttrBuilder.get('DictionaryAttr')(impl_opts, context=_ods_context))
    results.extend(outputs)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def impl_type(self):
    return _ods_ir.StringAttr(self.operation.attributes["impl_type"])

  @impl_type.setter
  def impl_type(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["impl_type"] = value

  @builtins.property
  def outputs(self):
    _ods_variadic_group_length = len(self.operation.results) - 1 + 1
    return self.operation.results[0:0 + _ods_variadic_group_length]

  @builtins.property
  def portReqs(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ServiceInstanceOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.instance"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, impl_type, inputs, *, service_symbol=None, impl_opts=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    _ods_context = _ods_get_default_loc_context(loc)
    if service_symbol is not None: attributes["service_symbol"] = (service_symbol if (
        issubclass(type(service_symbol), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('FlatSymbolRefAttr')) else
          _ods_ir.AttrBuilder.get('FlatSymbolRefAttr')(service_symbol, context=_ods_context))
    attributes["impl_type"] = (impl_type if (
    issubclass(type(impl_type), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('StrAttr')) else
      _ods_ir.AttrBuilder.get('StrAttr')(impl_type, context=_ods_context))
    if impl_opts is not None: attributes["impl_opts"] = (impl_opts if (
        issubclass(type(impl_opts), _ods_ir.Attribute) or
        not _ods_ir.AttrBuilder.contains('DictionaryAttr')) else
          _ods_ir.AttrBuilder.get('DictionaryAttr')(impl_opts, context=_ods_context))
    results.extend(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def impl_type(self):
    return _ods_ir.StringAttr(self.operation.attributes["impl_type"])

  @impl_type.setter
  def impl_type(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["impl_type"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ToClientOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.to_client"

  _ODS_REGIONS = (0, True)

  def __init__(self, inner_sym, toClientType, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["inner_sym"] = (inner_sym if (
    issubclass(type(inner_sym), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(inner_sym, context=_ods_context))
    attributes["toClientType"] = (toClientType if (
    issubclass(type(toClientType), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(toClientType, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inner_sym(self):
    return _ods_ir.StringAttr(self.operation.attributes["inner_sym"])

  @inner_sym.setter
  def inner_sym(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["inner_sym"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ToServerOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.service.to_server"

  _ODS_REGIONS = (0, True)

  def __init__(self, inner_sym, toServerType, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    _ods_context = _ods_get_default_loc_context(loc)
    attributes["inner_sym"] = (inner_sym if (
    issubclass(type(inner_sym), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('SymbolNameAttr')) else
      _ods_ir.AttrBuilder.get('SymbolNameAttr')(inner_sym, context=_ods_context))
    attributes["toServerType"] = (toServerType if (
    issubclass(type(toServerType), _ods_ir.Attribute) or
    not _ods_ir.AttrBuilder.contains('TypeAttr')) else
      _ods_ir.AttrBuilder.get('TypeAttr')(toServerType, context=_ods_context))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inner_sym(self):
    return _ods_ir.StringAttr(self.operation.attributes["inner_sym"])

  @inner_sym.setter
  def inner_sym(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["inner_sym"] = value

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class UnwrapFIFOOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.unwrap.fifo"

  _ODS_REGIONS = (0, True)

  def __init__(self, chanInput, rden, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(chanInput))
    operands.append(_get_op_result_or_value(rden))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(UnwrapFIFOOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def chanInput(self):
    return self.operation.operands[0]

  @builtins.property
  def rden(self):
    return self.operation.operands[1]

  @builtins.property
  def data(self):
    return self.operation.results[0]

  @builtins.property
  def empty(self):
    return self.operation.results[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class UnwrapSVInterfaceOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.unwrap.iface"

  _ODS_REGIONS = (0, True)

  def __init__(self, chanInput, interfaceSource, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(chanInput))
    operands.append(_get_op_result_or_value(interfaceSource))
    _ods_context = _ods_get_default_loc_context(loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def chanInput(self):
    return self.operation.operands[0]

  @builtins.property
  def interfaceSource(self):
    return self.operation.operands[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class UnwrapValidReadyOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.unwrap.vr"

  _ODS_REGIONS = (0, True)

  def __init__(self, rawOutput, valid, chanInput, ready, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(chanInput))
    operands.append(_get_op_result_or_value(ready))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(rawOutput)
    results.append(valid)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def chanInput(self):
    return self.operation.operands[0]

  @builtins.property
  def ready(self):
    return self.operation.operands[1]

  @builtins.property
  def rawOutput(self):
    return self.operation.results[0]

  @builtins.property
  def valid(self):
    return self.operation.results[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class UnwrapWindow(_ods_ir.OpView):
  OPERATION_NAME = "esi.window.unwrap"

  _ODS_REGIONS = (0, True)

  def __init__(self, window, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(window))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(UnwrapWindow).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def window(self):
    return self.operation.operands[0]

  @builtins.property
  def frame(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class WrapFIFOOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.wrap.fifo"

  _ODS_REGIONS = (0, True)

  def __init__(self, chanOutput, rden, data, empty, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(data))
    operands.append(_get_op_result_or_value(empty))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(chanOutput)
    results.append(rden)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def data(self):
    return self.operation.operands[0]

  @builtins.property
  def empty(self):
    return self.operation.operands[1]

  @builtins.property
  def chanOutput(self):
    return self.operation.results[0]

  @builtins.property
  def rden(self):
    return self.operation.results[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class WrapSVInterfaceOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.wrap.iface"

  _ODS_REGIONS = (0, True)

  def __init__(self, output, interfaceSink, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(interfaceSink))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(output)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def interfaceSink(self):
    return self.operation.operands[0]

  @builtins.property
  def output(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class WrapValidReadyOp(_ods_ir.OpView):
  OPERATION_NAME = "esi.wrap.vr"

  _ODS_REGIONS = (0, True)

  def __init__(self, chanOutput, ready, rawInput, valid, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(rawInput))
    operands.append(_get_op_result_or_value(valid))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(chanOutput)
    results.append(ready)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def rawInput(self):
    return self.operation.operands[0]

  @builtins.property
  def valid(self):
    return self.operation.operands[1]

  @builtins.property
  def chanOutput(self):
    return self.operation.results[0]

  @builtins.property
  def ready(self):
    return self.operation.results[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class WrapWindow(_ods_ir.OpView):
  OPERATION_NAME = "esi.window.wrap"

  _ODS_REGIONS = (0, True)

  def __init__(self, window, frame, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(frame))
    _ods_context = _ods_get_default_loc_context(loc)
    results.append(window)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def frame(self):
    return self.operation.operands[0]

  @builtins.property
  def window(self):
    return self.operation.results[0]
