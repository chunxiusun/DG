# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: importer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import matrix_pb2 as matrix__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='importer.proto',
  package='dg.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x0eimporter.proto\x12\x08\x64g.proto\x1a\x0cmatrix.proto\"E\n\x0cSensorFilter\x12\x18\n\x10QualityThreshold\x18\x01 \x01(\x02\x12\x1b\n\x13IsRemoveDuplication\x18\x02 \x01(\x08\"f\n\x0eImporterResult\x12&\n\tRecResult\x18\x01 \x01(\x0b\x32\x13.dg.proto.RecResult\x12,\n\x0cSensorFilter\x18\x02 \x01(\x0b\x32\x16.dg.proto.SensorFilterb\x06proto3')
  ,
  dependencies=[matrix__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SENSORFILTER = _descriptor.Descriptor(
  name='SensorFilter',
  full_name='dg.proto.SensorFilter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='QualityThreshold', full_name='dg.proto.SensorFilter.QualityThreshold', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='IsRemoveDuplication', full_name='dg.proto.SensorFilter.IsRemoveDuplication', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=111,
)


_IMPORTERRESULT = _descriptor.Descriptor(
  name='ImporterResult',
  full_name='dg.proto.ImporterResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='RecResult', full_name='dg.proto.ImporterResult.RecResult', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='SensorFilter', full_name='dg.proto.ImporterResult.SensorFilter', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=215,
)

_IMPORTERRESULT.fields_by_name['RecResult'].message_type = matrix__pb2._RECRESULT
_IMPORTERRESULT.fields_by_name['SensorFilter'].message_type = _SENSORFILTER
DESCRIPTOR.message_types_by_name['SensorFilter'] = _SENSORFILTER
DESCRIPTOR.message_types_by_name['ImporterResult'] = _IMPORTERRESULT

SensorFilter = _reflection.GeneratedProtocolMessageType('SensorFilter', (_message.Message,), dict(
  DESCRIPTOR = _SENSORFILTER,
  __module__ = 'importer_pb2'
  # @@protoc_insertion_point(class_scope:dg.proto.SensorFilter)
  ))
_sym_db.RegisterMessage(SensorFilter)

ImporterResult = _reflection.GeneratedProtocolMessageType('ImporterResult', (_message.Message,), dict(
  DESCRIPTOR = _IMPORTERRESULT,
  __module__ = 'importer_pb2'
  # @@protoc_insertion_point(class_scope:dg.proto.ImporterResult)
  ))
_sym_db.RegisterMessage(ImporterResult)


# @@protoc_insertion_point(module_scope)
