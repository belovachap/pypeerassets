# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: 0005-on-chain-voting-transaction-specification.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='0005-on-chain-voting-transaction-specification.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n40005-on-chain-voting-transaction-specification.proto\"\xb5\x01\n\x04Vote\x12\x0f\n\x07version\x18\x01 \x01(\r\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncount_mode\x18\x03 \x01(\r\x12\x0f\n\x07\x63hoices\x18\x04 \x03(\t\x12\x15\n\rvote_metainfo\x18\x05 \x01(\x0c\"K\n\x04MODE\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06SIMPLE\x10\x01\x12\x17\n\x13WEIGHT_CARD_BALANCE\x10\x03\x12\x14\n\x10WEIGHT_CARD_DAYS\x10\x07\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_VOTE_MODE = _descriptor.EnumDescriptor(
  name='MODE',
  full_name='Vote.MODE',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NONE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SIMPLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEIGHT_CARD_BALANCE', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WEIGHT_CARD_DAYS', index=3, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=163,
  serialized_end=238,
)
_sym_db.RegisterEnumDescriptor(_VOTE_MODE)


_VOTE = _descriptor.Descriptor(
  name='Vote',
  full_name='Vote',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='Vote.version', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='description', full_name='Vote.description', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='count_mode', full_name='Vote.count_mode', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='choices', full_name='Vote.choices', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vote_metainfo', full_name='Vote.vote_metainfo', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _VOTE_MODE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=238,
)

_VOTE_MODE.containing_type = _VOTE
DESCRIPTOR.message_types_by_name['Vote'] = _VOTE

Vote = _reflection.GeneratedProtocolMessageType('Vote', (_message.Message,), dict(
  DESCRIPTOR = _VOTE,
  __module__ = '0005_on_chain_voting_transaction_specification_pb2'
  # @@protoc_insertion_point(class_scope:Vote)
  ))
_sym_db.RegisterMessage(Vote)


# @@protoc_insertion_point(module_scope)
