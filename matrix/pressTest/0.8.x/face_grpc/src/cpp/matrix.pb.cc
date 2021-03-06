// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: matrix.proto

#define INTERNAL_SUPPRESS_PROTOBUF_FIELD_DEPRECATION
#include "matrix.pb.h"

#include <algorithm>

#include <google/protobuf/stubs/common.h>
#include <google/protobuf/stubs/port.h>
#include <google/protobuf/stubs/once.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/wire_format_lite_inl.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)

namespace dg {
namespace model {

namespace {


}  // namespace


void protobuf_AssignDesc_matrix_2eproto() {
  protobuf_AddDesc_matrix_2eproto();
  const ::google::protobuf::FileDescriptor* file =
    ::google::protobuf::DescriptorPool::generated_pool()->FindFileByName(
      "matrix.proto");
  GOOGLE_CHECK(file != NULL);
}

namespace {

GOOGLE_PROTOBUF_DECLARE_ONCE(protobuf_AssignDescriptors_once_);
inline void protobuf_AssignDescriptorsOnce() {
  ::google::protobuf::GoogleOnceInit(&protobuf_AssignDescriptors_once_,
                 &protobuf_AssignDesc_matrix_2eproto);
}

void protobuf_RegisterTypes(const ::std::string&) {
  protobuf_AssignDescriptorsOnce();
}

}  // namespace

void protobuf_ShutdownFile_matrix_2eproto() {
}

void protobuf_AddDesc_matrix_2eproto() {
  static bool already_here = false;
  if (already_here) return;
  already_here = true;
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  ::dg::model::protobuf_AddDesc_system_2eproto();
  ::dg::model::protobuf_AddDesc_witness_2eproto();
  ::dg::model::protobuf_AddDesc_skynet_2eproto();
  ::dg::model::protobuf_AddDesc_ranker_2eproto();
  ::google::protobuf::DescriptorPool::InternalAddGeneratedFile(
    "\n\014matrix.proto\022\010dg.model\032\014system.proto\032\r"
    "witness.proto\032\014skynet.proto\032\014ranker.prot"
    "o2\200\005\n\rMatrixService\0227\n\004Ping\022\025.dg.model.P"
    "ingRequest\032\026.dg.model.PingResponse\"\000\022O\n\014"
    "SystemStatus\022\035.dg.model.SystemStatusRequ"
    "est\032\036.dg.model.SystemStatusResponse\"\000\022T\n"
    "\014GetInstances\022\035.dg.model.GetInstancesReq"
    "uest\032#.dg.model.InstanceConfigureRespons"
    "e\"\000\022Y\n\014ConfigEngine\022\".dg.model.InstanceC"
    "onfigureRequest\032#.dg.model.InstanceConfi"
    "gureResponse\"\000\022B\n\tRecognize\022\030.dg.model.W"
    "itnessRequest\032\031.dg.model.WitnessResponse"
    "\"\000\022Q\n\016BatchRecognize\022\035.dg.model.WitnessB"
    "atchRequest\032\036.dg.model.WitnessBatchRespo"
    "nse\"\000\022E\n\016VideoRecognize\022\027.dg.model.Skyne"
    "tRequest\032\030.dg.model.SkynetResponse\"\000\022V\n\017"
    "GetRankedVector\022\037.dg.model.FeatureRankin"
    "gRequest\032 .dg.model.FeatureRankingRespon"
    "se\"\000b\006proto3", 732);
  ::google::protobuf::MessageFactory::InternalRegisterGeneratedFile(
    "matrix.proto", &protobuf_RegisterTypes);
  ::google::protobuf::internal::OnShutdown(&protobuf_ShutdownFile_matrix_2eproto);
}

// Force AddDescriptors() to be called at static initialization time.
struct StaticDescriptorInitializer_matrix_2eproto {
  StaticDescriptorInitializer_matrix_2eproto() {
    protobuf_AddDesc_matrix_2eproto();
  }
} static_descriptor_initializer_matrix_2eproto_;

// @@protoc_insertion_point(namespace_scope)

}  // namespace model
}  // namespace dg

// @@protoc_insertion_point(global_scope)
