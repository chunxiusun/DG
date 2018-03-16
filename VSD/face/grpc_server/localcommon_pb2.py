# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: localcommon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='localcommon.proto',
  package='dg.model',
  syntax='proto3',
  serialized_pb=_b('\n\x11localcommon.proto\x12\x08\x64g.model\")\n\x04Time\x12\x0f\n\x07Seconds\x18\x01 \x01(\x03\x12\x10\n\x08NanoSecs\x18\x02 \x01(\x03\",\n\x0bMatrixError\x12\x0c\n\x04\x43ode\x18\x01 \x01(\x05\x12\x0f\n\x07Message\x18\x02 \x01(\t*`\n\rRecognizeType\x12\x14\n\x10REC_TYPE_DEFAULT\x10\x00\x12\x14\n\x10REC_TYPE_VEHICLE\x10\x01\x12\x11\n\rREC_TYPE_FACE\x10\x02\x12\x10\n\x0cREC_TYPE_ALL\x10\x03*L\n\x08RankType\x12\x15\n\x11RANK_TYPE_DEFAULT\x10\x00\x12\x15\n\x11RANK_TYPE_VEHICLE\x10\x01\x12\x12\n\x0eRANK_TYPE_FACE\x10\x02*\xdb\x03\n\x12RecognizeFunctions\x12\x10\n\x0cRECFUNC_NONE\x10\x00\x12\x13\n\x0fRECFUNC_VEHICLE\x10\x01\x12\x1a\n\x16RECFUNC_VEHICLE_DETECT\x10\n\x12\x19\n\x15RECFUNC_VEHICLE_TRACK\x10\x0b\x12\x19\n\x15RECFUNC_VEHICLE_STYLE\x10\x0c\x12\x19\n\x15RECFUNC_VEHICLE_COLOR\x10\r\x12\x1a\n\x16RECFUNC_VEHICLE_MARKER\x10\x0e\x12\x19\n\x15RECFUNC_VEHICLE_PLATE\x10\x0f\x12\"\n\x1eRECFUNC_VEHICLE_FEATURE_VECTOR\x10\x10\x12\"\n\x1dRECFUNC_VEHICLE_DRIVER_NOBELT\x10\xaa\x01\x12!\n\x1cRECFUNC_VEHICLE_DRIVER_PHONE\x10\xab\x01\x12$\n\x1fRECFUNC_VEHICLE_CODRIVER_NOBELT\x10\xac\x01\x12\x10\n\x0cRECFUNC_FACE\x10\x02\x12\x19\n\x15RECFUNC_FACE_DETECTOR\x10\x14\x12\x1f\n\x1bRECFUNC_FACE_FEATURE_VECTOR\x10\x15\x12\x1b\n\x17RECFUNC_PEDESTRIAN_ATTR\x10\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_RECOGNIZETYPE = _descriptor.EnumDescriptor(
  name='RecognizeType',
  full_name='dg.model.RecognizeType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='REC_TYPE_DEFAULT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REC_TYPE_VEHICLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REC_TYPE_FACE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REC_TYPE_ALL', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=120,
  serialized_end=216,
)
_sym_db.RegisterEnumDescriptor(_RECOGNIZETYPE)

RecognizeType = enum_type_wrapper.EnumTypeWrapper(_RECOGNIZETYPE)
_RANKTYPE = _descriptor.EnumDescriptor(
  name='RankType',
  full_name='dg.model.RankType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RANK_TYPE_DEFAULT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RANK_TYPE_VEHICLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RANK_TYPE_FACE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=218,
  serialized_end=294,
)
_sym_db.RegisterEnumDescriptor(_RANKTYPE)

RankType = enum_type_wrapper.EnumTypeWrapper(_RANKTYPE)
_RECOGNIZEFUNCTIONS = _descriptor.EnumDescriptor(
  name='RecognizeFunctions',
  full_name='dg.model.RecognizeFunctions',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_DETECT', index=2, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_TRACK', index=3, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_STYLE', index=4, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_COLOR', index=5, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_MARKER', index=6, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_PLATE', index=7, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_FEATURE_VECTOR', index=8, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_DRIVER_NOBELT', index=9, number=170,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_DRIVER_PHONE', index=10, number=171,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_VEHICLE_CODRIVER_NOBELT', index=11, number=172,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_FACE', index=12, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_FACE_DETECTOR', index=13, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_FACE_FEATURE_VECTOR', index=14, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RECFUNC_PEDESTRIAN_ATTR', index=15, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=297,
  serialized_end=772,
)
_sym_db.RegisterEnumDescriptor(_RECOGNIZEFUNCTIONS)

RecognizeFunctions = enum_type_wrapper.EnumTypeWrapper(_RECOGNIZEFUNCTIONS)
REC_TYPE_DEFAULT = 0
REC_TYPE_VEHICLE = 1
REC_TYPE_FACE = 2
REC_TYPE_ALL = 3
RANK_TYPE_DEFAULT = 0
RANK_TYPE_VEHICLE = 1
RANK_TYPE_FACE = 2
RECFUNC_NONE = 0
RECFUNC_VEHICLE = 1
RECFUNC_VEHICLE_DETECT = 10
RECFUNC_VEHICLE_TRACK = 11
RECFUNC_VEHICLE_STYLE = 12
RECFUNC_VEHICLE_COLOR = 13
RECFUNC_VEHICLE_MARKER = 14
RECFUNC_VEHICLE_PLATE = 15
RECFUNC_VEHICLE_FEATURE_VECTOR = 16
RECFUNC_VEHICLE_DRIVER_NOBELT = 170
RECFUNC_VEHICLE_DRIVER_PHONE = 171
RECFUNC_VEHICLE_CODRIVER_NOBELT = 172
RECFUNC_FACE = 2
RECFUNC_FACE_DETECTOR = 20
RECFUNC_FACE_FEATURE_VECTOR = 21
RECFUNC_PEDESTRIAN_ATTR = 3



_TIME = _descriptor.Descriptor(
  name='Time',
  full_name='dg.model.Time',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Seconds', full_name='dg.model.Time.Seconds', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='NanoSecs', full_name='dg.model.Time.NanoSecs', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=31,
  serialized_end=72,
)


_MATRIXERROR = _descriptor.Descriptor(
  name='MatrixError',
  full_name='dg.model.MatrixError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='Code', full_name='dg.model.MatrixError.Code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='Message', full_name='dg.model.MatrixError.Message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=74,
  serialized_end=118,
)

DESCRIPTOR.message_types_by_name['Time'] = _TIME
DESCRIPTOR.message_types_by_name['MatrixError'] = _MATRIXERROR
DESCRIPTOR.enum_types_by_name['RecognizeType'] = _RECOGNIZETYPE
DESCRIPTOR.enum_types_by_name['RankType'] = _RANKTYPE
DESCRIPTOR.enum_types_by_name['RecognizeFunctions'] = _RECOGNIZEFUNCTIONS

Time = _reflection.GeneratedProtocolMessageType('Time', (_message.Message,), dict(
  DESCRIPTOR = _TIME,
  __module__ = 'localcommon_pb2'
  # @@protoc_insertion_point(class_scope:dg.model.Time)
  ))
_sym_db.RegisterMessage(Time)

MatrixError = _reflection.GeneratedProtocolMessageType('MatrixError', (_message.Message,), dict(
  DESCRIPTOR = _MATRIXERROR,
  __module__ = 'localcommon_pb2'
  # @@protoc_insertion_point(class_scope:dg.model.MatrixError)
  ))
_sym_db.RegisterMessage(MatrixError)


import grpc
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities
# @@protoc_insertion_point(module_scope)