// Generated by the gRPC protobuf plugin.
// If you make any local change, they will be lost.
// source: witness.proto

#include "witness.pb.h"
#include "witness.grpc.pb.h"

#include <grpc++/impl/codegen/async_stream.h>
#include <grpc++/impl/codegen/async_unary_call.h>
#include <grpc++/impl/codegen/channel_interface.h>
#include <grpc++/impl/codegen/client_unary_call.h>
#include <grpc++/impl/codegen/method_handler_impl.h>
#include <grpc++/impl/codegen/rpc_service_method.h>
#include <grpc++/impl/codegen/service_type.h>
#include <grpc++/impl/codegen/sync_stream.h>
namespace dg {
namespace model {

static const char* WitnessService_method_names[] = {
  "/dg.model.WitnessService/Recognize",
  "/dg.model.WitnessService/BatchRecognize",
  "/dg.model.WitnessService/GetIndex",
  "/dg.model.WitnessService/GetIndexTxt",
};

std::unique_ptr< WitnessService::Stub> WitnessService::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  std::unique_ptr< WitnessService::Stub> stub(new WitnessService::Stub(channel));
  return stub;
}

WitnessService::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel)
  : channel_(channel), rpcmethod_Recognize_(WitnessService_method_names[0], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_BatchRecognize_(WitnessService_method_names[1], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_GetIndex_(WitnessService_method_names[2], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_GetIndexTxt_(WitnessService_method_names[3], ::grpc::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status WitnessService::Stub::Recognize(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::dg::model::WitnessResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_Recognize_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::WitnessResponse>* WitnessService::Stub::AsyncRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessResponse>(channel_.get(), cq, rpcmethod_Recognize_, context, request);
}

::grpc::Status WitnessService::Stub::BatchRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::dg::model::WitnessBatchResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_BatchRecognize_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::WitnessBatchResponse>* WitnessService::Stub::AsyncBatchRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessBatchResponse>(channel_.get(), cq, rpcmethod_BatchRecognize_, context, request);
}

::grpc::Status WitnessService::Stub::GetIndex(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::dg::model::IndexResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_GetIndex_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::IndexResponse>* WitnessService::Stub::AsyncGetIndexRaw(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::IndexResponse>(channel_.get(), cq, rpcmethod_GetIndex_, context, request);
}

::grpc::Status WitnessService::Stub::GetIndexTxt(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::dg::model::IndexTxtResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_GetIndexTxt_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::IndexTxtResponse>* WitnessService::Stub::AsyncGetIndexTxtRaw(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::IndexTxtResponse>(channel_.get(), cq, rpcmethod_GetIndexTxt_, context, request);
}

WitnessService::Service::Service() {
  (void)WitnessService_method_names;
  AddMethod(new ::grpc::RpcServiceMethod(
      WitnessService_method_names[0],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< WitnessService::Service, ::dg::model::WitnessRequest, ::dg::model::WitnessResponse>(
          std::mem_fn(&WitnessService::Service::Recognize), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      WitnessService_method_names[1],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< WitnessService::Service, ::dg::model::WitnessBatchRequest, ::dg::model::WitnessBatchResponse>(
          std::mem_fn(&WitnessService::Service::BatchRecognize), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      WitnessService_method_names[2],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< WitnessService::Service, ::dg::model::IndexRequest, ::dg::model::IndexResponse>(
          std::mem_fn(&WitnessService::Service::GetIndex), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      WitnessService_method_names[3],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< WitnessService::Service, ::dg::model::IndexTxtRequest, ::dg::model::IndexTxtResponse>(
          std::mem_fn(&WitnessService::Service::GetIndexTxt), this)));
}

WitnessService::Service::~Service() {
}

::grpc::Status WitnessService::Service::Recognize(::grpc::ServerContext* context, const ::dg::model::WitnessRequest* request, ::dg::model::WitnessResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status WitnessService::Service::BatchRecognize(::grpc::ServerContext* context, const ::dg::model::WitnessBatchRequest* request, ::dg::model::WitnessBatchResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status WitnessService::Service::GetIndex(::grpc::ServerContext* context, const ::dg::model::IndexRequest* request, ::dg::model::IndexResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status WitnessService::Service::GetIndexTxt(::grpc::ServerContext* context, const ::dg::model::IndexTxtRequest* request, ::dg::model::IndexTxtResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace dg
}  // namespace model

