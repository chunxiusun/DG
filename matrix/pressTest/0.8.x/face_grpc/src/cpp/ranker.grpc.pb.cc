// Generated by the gRPC protobuf plugin.
// If you make any local change, they will be lost.
// source: ranker.proto

#include "ranker.pb.h"
#include "ranker.grpc.pb.h"

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

static const char* SimilarityService_method_names[] = {
  "/dg.model.SimilarityService/RankImage",
  "/dg.model.SimilarityService/RankFeature",
  "/dg.model.SimilarityService/RankFeaturesPair",
  "/dg.model.SimilarityService/AddFeatures",
  "/dg.model.SimilarityService/GetImageContent",
  "/dg.model.SimilarityService/Search",
  "/dg.model.SimilarityService/RankRepoSize",
  "/dg.model.SimilarityService/GetRankedVector",
};

std::unique_ptr< SimilarityService::Stub> SimilarityService::NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options) {
  std::unique_ptr< SimilarityService::Stub> stub(new SimilarityService::Stub(channel));
  return stub;
}

SimilarityService::Stub::Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel)
  : channel_(channel), rpcmethod_RankImage_(SimilarityService_method_names[0], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_RankFeature_(SimilarityService_method_names[1], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_RankFeaturesPair_(SimilarityService_method_names[2], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_AddFeatures_(SimilarityService_method_names[3], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_GetImageContent_(SimilarityService_method_names[4], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_Search_(SimilarityService_method_names[5], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_RankRepoSize_(SimilarityService_method_names[6], ::grpc::RpcMethod::NORMAL_RPC, channel)
  , rpcmethod_GetRankedVector_(SimilarityService_method_names[7], ::grpc::RpcMethod::NORMAL_RPC, channel)
  {}

::grpc::Status SimilarityService::Stub::RankImage(::grpc::ClientContext* context, const ::dg::model::RankImageRequest& request, ::dg::model::RankImageResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_RankImage_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::RankImageResponse>* SimilarityService::Stub::AsyncRankImageRaw(::grpc::ClientContext* context, const ::dg::model::RankImageRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::RankImageResponse>(channel_.get(), cq, rpcmethod_RankImage_, context, request);
}

::grpc::Status SimilarityService::Stub::RankFeature(::grpc::ClientContext* context, const ::dg::model::RankFeatureRequest& request, ::dg::model::RankFeatureResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_RankFeature_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::RankFeatureResponse>* SimilarityService::Stub::AsyncRankFeatureRaw(::grpc::ClientContext* context, const ::dg::model::RankFeatureRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::RankFeatureResponse>(channel_.get(), cq, rpcmethod_RankFeature_, context, request);
}

::grpc::Status SimilarityService::Stub::RankFeaturesPair(::grpc::ClientContext* context, const ::dg::model::RankFeaturesPairRequest& request, ::dg::model::RankFeaturesPairResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_RankFeaturesPair_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::RankFeaturesPairResponse>* SimilarityService::Stub::AsyncRankFeaturesPairRaw(::grpc::ClientContext* context, const ::dg::model::RankFeaturesPairRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::RankFeaturesPairResponse>(channel_.get(), cq, rpcmethod_RankFeaturesPair_, context, request);
}

::grpc::Status SimilarityService::Stub::AddFeatures(::grpc::ClientContext* context, const ::dg::model::AddFeaturesRequest& request, ::dg::model::AddFeaturesResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_AddFeatures_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::AddFeaturesResponse>* SimilarityService::Stub::AsyncAddFeaturesRaw(::grpc::ClientContext* context, const ::dg::model::AddFeaturesRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::AddFeaturesResponse>(channel_.get(), cq, rpcmethod_AddFeatures_, context, request);
}

::grpc::Status SimilarityService::Stub::GetImageContent(::grpc::ClientContext* context, const ::dg::model::GetImageContentRequest& request, ::dg::model::GetImageContentResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_GetImageContent_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::GetImageContentResponse>* SimilarityService::Stub::AsyncGetImageContentRaw(::grpc::ClientContext* context, const ::dg::model::GetImageContentRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::GetImageContentResponse>(channel_.get(), cq, rpcmethod_GetImageContent_, context, request);
}

::grpc::Status SimilarityService::Stub::Search(::grpc::ClientContext* context, const ::dg::model::SearchRequest& request, ::dg::model::SearchResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_Search_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::SearchResponse>* SimilarityService::Stub::AsyncSearchRaw(::grpc::ClientContext* context, const ::dg::model::SearchRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::SearchResponse>(channel_.get(), cq, rpcmethod_Search_, context, request);
}

::grpc::Status SimilarityService::Stub::RankRepoSize(::grpc::ClientContext* context, const ::dg::model::RankRepoSizeRequest& request, ::dg::model::RankRepoSizeResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_RankRepoSize_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::RankRepoSizeResponse>* SimilarityService::Stub::AsyncRankRepoSizeRaw(::grpc::ClientContext* context, const ::dg::model::RankRepoSizeRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::RankRepoSizeResponse>(channel_.get(), cq, rpcmethod_RankRepoSize_, context, request);
}

::grpc::Status SimilarityService::Stub::GetRankedVector(::grpc::ClientContext* context, const ::dg::model::FeatureRankingRequest& request, ::dg::model::FeatureRankingResponse* response) {
  return ::grpc::BlockingUnaryCall(channel_.get(), rpcmethod_GetRankedVector_, context, request, response);
}

::grpc::ClientAsyncResponseReader< ::dg::model::FeatureRankingResponse>* SimilarityService::Stub::AsyncGetRankedVectorRaw(::grpc::ClientContext* context, const ::dg::model::FeatureRankingRequest& request, ::grpc::CompletionQueue* cq) {
  return new ::grpc::ClientAsyncResponseReader< ::dg::model::FeatureRankingResponse>(channel_.get(), cq, rpcmethod_GetRankedVector_, context, request);
}

SimilarityService::Service::Service() {
  (void)SimilarityService_method_names;
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[0],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::RankImageRequest, ::dg::model::RankImageResponse>(
          std::mem_fn(&SimilarityService::Service::RankImage), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[1],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::RankFeatureRequest, ::dg::model::RankFeatureResponse>(
          std::mem_fn(&SimilarityService::Service::RankFeature), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[2],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::RankFeaturesPairRequest, ::dg::model::RankFeaturesPairResponse>(
          std::mem_fn(&SimilarityService::Service::RankFeaturesPair), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[3],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::AddFeaturesRequest, ::dg::model::AddFeaturesResponse>(
          std::mem_fn(&SimilarityService::Service::AddFeatures), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[4],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::GetImageContentRequest, ::dg::model::GetImageContentResponse>(
          std::mem_fn(&SimilarityService::Service::GetImageContent), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[5],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::SearchRequest, ::dg::model::SearchResponse>(
          std::mem_fn(&SimilarityService::Service::Search), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[6],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::RankRepoSizeRequest, ::dg::model::RankRepoSizeResponse>(
          std::mem_fn(&SimilarityService::Service::RankRepoSize), this)));
  AddMethod(new ::grpc::RpcServiceMethod(
      SimilarityService_method_names[7],
      ::grpc::RpcMethod::NORMAL_RPC,
      new ::grpc::RpcMethodHandler< SimilarityService::Service, ::dg::model::FeatureRankingRequest, ::dg::model::FeatureRankingResponse>(
          std::mem_fn(&SimilarityService::Service::GetRankedVector), this)));
}

SimilarityService::Service::~Service() {
}

::grpc::Status SimilarityService::Service::RankImage(::grpc::ServerContext* context, const ::dg::model::RankImageRequest* request, ::dg::model::RankImageResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::RankFeature(::grpc::ServerContext* context, const ::dg::model::RankFeatureRequest* request, ::dg::model::RankFeatureResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::RankFeaturesPair(::grpc::ServerContext* context, const ::dg::model::RankFeaturesPairRequest* request, ::dg::model::RankFeaturesPairResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::AddFeatures(::grpc::ServerContext* context, const ::dg::model::AddFeaturesRequest* request, ::dg::model::AddFeaturesResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::GetImageContent(::grpc::ServerContext* context, const ::dg::model::GetImageContentRequest* request, ::dg::model::GetImageContentResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::Search(::grpc::ServerContext* context, const ::dg::model::SearchRequest* request, ::dg::model::SearchResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::RankRepoSize(::grpc::ServerContext* context, const ::dg::model::RankRepoSizeRequest* request, ::dg::model::RankRepoSizeResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}

::grpc::Status SimilarityService::Service::GetRankedVector(::grpc::ServerContext* context, const ::dg::model::FeatureRankingRequest* request, ::dg::model::FeatureRankingResponse* response) {
  (void) context;
  (void) request;
  (void) response;
  return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
}


}  // namespace dg
}  // namespace model
