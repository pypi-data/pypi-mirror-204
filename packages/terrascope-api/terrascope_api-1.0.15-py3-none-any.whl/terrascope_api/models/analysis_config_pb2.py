# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: analysis_config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from terrascope_api.models import common_models_pb2 as common__models__pb2
from terrascope_api.models import analysis_pb2 as analysis__pb2
try:
  common__models__pb2 = analysis__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__pb2.common_models_pb2
from terrascope_api.models import analysis_version_pb2 as analysis__version__pb2
try:
  common__models__pb2 = analysis__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__version__pb2.common_models_pb2
try:
  analysis__pb2 = analysis__version__pb2.analysis__pb2
except AttributeError:
  analysis__pb2 = analysis__version__pb2.analysis_pb2
try:
  common__models__pb2 = analysis__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__version__pb2.common_models_pb2
try:
  algorithm__version__pb2 = analysis__version__pb2.algorithm__version__pb2
except AttributeError:
  algorithm__version__pb2 = analysis__version__pb2.algorithm_version_pb2
try:
  common__models__pb2 = analysis__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__version__pb2.common_models_pb2
try:
  algorithm__pb2 = analysis__version__pb2.algorithm__pb2
except AttributeError:
  algorithm__pb2 = analysis__version__pb2.algorithm_pb2
try:
  common__models__pb2 = analysis__version__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = analysis__version__pb2.common_models_pb2
from terrascope_api.models import algorithm_config_pb2 as algorithm__config__pb2
try:
  common__models__pb2 = algorithm__config__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__config__pb2.common_models_pb2
try:
  algorithm__pb2 = algorithm__config__pb2.algorithm__pb2
except AttributeError:
  algorithm__pb2 = algorithm__config__pb2.algorithm_pb2
try:
  common__models__pb2 = algorithm__config__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__config__pb2.common_models_pb2
try:
  algorithm__version__pb2 = algorithm__config__pb2.algorithm__version__pb2
except AttributeError:
  algorithm__version__pb2 = algorithm__config__pb2.algorithm_version_pb2
try:
  common__models__pb2 = algorithm__config__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__config__pb2.common_models_pb2
try:
  algorithm__pb2 = algorithm__config__pb2.algorithm__pb2
except AttributeError:
  algorithm__pb2 = algorithm__config__pb2.algorithm_pb2
try:
  common__models__pb2 = algorithm__config__pb2.common__models__pb2
except AttributeError:
  common__models__pb2 = algorithm__config__pb2.common_models_pb2

from terrascope_api.models.common_models_pb2 import *
from terrascope_api.models.analysis_pb2 import *
from terrascope_api.models.analysis_version_pb2 import *
from terrascope_api.models.algorithm_config_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61nalysis_config.proto\x12\x07oi.papi\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x13\x63ommon_models.proto\x1a\x0e\x61nalysis.proto\x1a\x16\x61nalysis_version.proto\x1a\x16\x61lgorithm_config.proto\"\xf2\x02\n\x0e\x41nalysisConfig\x12#\n\x08\x61nalysis\x18\x01 \x01(\x0b\x32\x11.oi.papi.Analysis\x12\x32\n\x10\x61nalysis_version\x18\x02 \x01(\x0b\x32\x18.oi.papi.AnalysisVersion\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12.\n\ncreated_on\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x44\n\x16\x61lgorithm_config_nodes\x18\x07 \x03(\x0b\x32$.oi.papi.AnalysisAlgorithmConfigNode\x12\x33\n\x11\x61lgorithm_configs\x18\x08 \x03(\x0b\x32\x18.oi.papi.AlgorithmConfig\x12\x15\n\ris_deprecated\x18\t \x01(\x08\x12\x16\n\x0eis_deactivated\x18\n \x01(\x08\"\xa3\x01\n\x1b\x41nalysisConfigCreateRequest\x12\x1b\n\x13\x61nalysis_version_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x44\n\x16\x61lgorithm_config_nodes\x18\x04 \x03(\x0b\x32$.oi.papi.AnalysisAlgorithmConfigNode\"e\n\x1c\x41nalysisConfigCreateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x30\n\x0f\x61nalysis_config\x18\x02 \x01(\x0b\x32\x17.oi.papi.AnalysisConfig\"\x92\x01\n\x1b\x41nalysisConfigUpdateRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x44\n\x16\x61lgorithm_config_nodes\x18\x04 \x03(\x0b\x32$.oi.papi.AnalysisAlgorithmConfigNode\"3\n\x1c\x41nalysisConfigUpdateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\"s\n\x18\x41nalysisConfigGetRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\x12!\n\x19include_algorithm_details\x18\x02 \x01(\x08\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x8c\x01\n\x19\x41nalysisConfigGetResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x31\n\x10\x61nalysis_configs\x18\x02 \x03(\x0b\x32\x17.oi.papi.AnalysisConfig\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\"\xa4\x02\n\x19\x41nalysisConfigListRequest\x12\x13\n\x0b\x61nalysis_id\x18\x01 \x01(\t\x12\x1b\n\x13\x61nalysis_version_id\x18\x02 \x01(\t\x12\x13\n\x0bsearch_text\x18\x03 \x01(\t\x12\x32\n\x0emin_created_on\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0emax_created_on\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1b\n\x13include_deactivated\x18\x06 \x01(\x08\x12\x12\n\nsubject_id\x18\x07 \x01(\t\x12\'\n\npagination\x18\x08 \x01(\x0b\x32\x13.oi.papi.Pagination\"\x8d\x01\n\x1a\x41nalysisConfigListResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r\x12\x31\n\x10\x61nalysis_configs\x18\x02 \x03(\x0b\x32\x17.oi.papi.AnalysisConfig\x12\'\n\npagination\x18\x03 \x01(\x0b\x32\x13.oi.papi.Pagination\".\n\x1f\x41nalysisConfigDeactivateRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"7\n AnalysisConfigDeactivateResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\r2\xc3\x03\n\x11\x41nalysisConfigApi\x12U\n\x06\x63reate\x12$.oi.papi.AnalysisConfigCreateRequest\x1a%.oi.papi.AnalysisConfigCreateResponse\x12U\n\x06update\x12$.oi.papi.AnalysisConfigUpdateRequest\x1a%.oi.papi.AnalysisConfigUpdateResponse\x12L\n\x03get\x12!.oi.papi.AnalysisConfigGetRequest\x1a\".oi.papi.AnalysisConfigGetResponse\x12O\n\x04list\x12\".oi.papi.AnalysisConfigListRequest\x1a#.oi.papi.AnalysisConfigListResponse\x12\x61\n\ndeactivate\x12(.oi.papi.AnalysisConfigDeactivateRequest\x1a).oi.papi.AnalysisConfigDeactivateResponseP\x01P\x02P\x03P\x04\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'analysis_config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ANALYSISCONFIG._serialized_start=153
  _ANALYSISCONFIG._serialized_end=523
  _ANALYSISCONFIGCREATEREQUEST._serialized_start=526
  _ANALYSISCONFIGCREATEREQUEST._serialized_end=689
  _ANALYSISCONFIGCREATERESPONSE._serialized_start=691
  _ANALYSISCONFIGCREATERESPONSE._serialized_end=792
  _ANALYSISCONFIGUPDATEREQUEST._serialized_start=795
  _ANALYSISCONFIGUPDATEREQUEST._serialized_end=941
  _ANALYSISCONFIGUPDATERESPONSE._serialized_start=943
  _ANALYSISCONFIGUPDATERESPONSE._serialized_end=994
  _ANALYSISCONFIGGETREQUEST._serialized_start=996
  _ANALYSISCONFIGGETREQUEST._serialized_end=1111
  _ANALYSISCONFIGGETRESPONSE._serialized_start=1114
  _ANALYSISCONFIGGETRESPONSE._serialized_end=1254
  _ANALYSISCONFIGLISTREQUEST._serialized_start=1257
  _ANALYSISCONFIGLISTREQUEST._serialized_end=1549
  _ANALYSISCONFIGLISTRESPONSE._serialized_start=1552
  _ANALYSISCONFIGLISTRESPONSE._serialized_end=1693
  _ANALYSISCONFIGDEACTIVATEREQUEST._serialized_start=1695
  _ANALYSISCONFIGDEACTIVATEREQUEST._serialized_end=1741
  _ANALYSISCONFIGDEACTIVATERESPONSE._serialized_start=1743
  _ANALYSISCONFIGDEACTIVATERESPONSE._serialized_end=1798
  _ANALYSISCONFIGAPI._serialized_start=1801
  _ANALYSISCONFIGAPI._serialized_end=2252
# @@protoc_insertion_point(module_scope)
