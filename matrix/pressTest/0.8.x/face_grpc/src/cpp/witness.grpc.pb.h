// Generated by the gRPC protobuf plugin.
// If you make any local change, they will be lost.
// source: witness.proto
#ifndef GRPC_witness_2eproto__INCLUDED
#define GRPC_witness_2eproto__INCLUDED

#include "witness.pb.h"

#include <grpc++/impl/codegen/async_stream.h>
#include <grpc++/impl/codegen/async_unary_call.h>
#include <grpc++/impl/codegen/proto_utils.h>
#include <grpc++/impl/codegen/rpc_method.h>
#include <grpc++/impl/codegen/service_type.h>
#include <grpc++/impl/codegen/status.h>
#include <grpc++/impl/codegen/stub_options.h>
#include <grpc++/impl/codegen/sync_stream.h>

namespace grpc {
class CompletionQueue;
class Channel;
class RpcService;
class ServerCompletionQueue;
class ServerContext;
}  // namespace grpc

namespace dg {
namespace model {

class WitnessService GRPC_FINAL {
 public:
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    virtual ::grpc::Status Recognize(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::dg::model::WitnessResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessResponse>> AsyncRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessResponse>>(AsyncRecognizeRaw(context, request, cq));
    }
    virtual ::grpc::Status BatchRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::dg::model::WitnessBatchResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessBatchResponse>> AsyncBatchRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessBatchResponse>>(AsyncBatchRecognizeRaw(context, request, cq));
    }
    virtual ::grpc::Status GetIndex(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::dg::model::IndexResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexResponse>> AsyncGetIndex(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexResponse>>(AsyncGetIndexRaw(context, request, cq));
    }
    virtual ::grpc::Status GetIndexTxt(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::dg::model::IndexTxtResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexTxtResponse>> AsyncGetIndexTxt(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexTxtResponse>>(AsyncGetIndexTxtRaw(context, request, cq));
    }
  private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessResponse>* AsyncRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::WitnessBatchResponse>* AsyncBatchRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexResponse>* AsyncGetIndexRaw(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::IndexTxtResponse>* AsyncGetIndexTxtRaw(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub GRPC_FINAL : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel);
    ::grpc::Status Recognize(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::dg::model::WitnessResponse* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessResponse>> AsyncRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessResponse>>(AsyncRecognizeRaw(context, request, cq));
    }
    ::grpc::Status BatchRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::dg::model::WitnessBatchResponse* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessBatchResponse>> AsyncBatchRecognize(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessBatchResponse>>(AsyncBatchRecognizeRaw(context, request, cq));
    }
    ::grpc::Status GetIndex(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::dg::model::IndexResponse* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::IndexResponse>> AsyncGetIndex(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::IndexResponse>>(AsyncGetIndexRaw(context, request, cq));
    }
    ::grpc::Status GetIndexTxt(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::dg::model::IndexTxtResponse* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::IndexTxtResponse>> AsyncGetIndexTxt(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::IndexTxtResponse>>(AsyncGetIndexTxtRaw(context, request, cq));
    }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessResponse>* AsyncRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessRequest& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    ::grpc::ClientAsyncResponseReader< ::dg::model::WitnessBatchResponse>* AsyncBatchRecognizeRaw(::grpc::ClientContext* context, const ::dg::model::WitnessBatchRequest& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    ::grpc::ClientAsyncResponseReader< ::dg::model::IndexResponse>* AsyncGetIndexRaw(::grpc::ClientContext* context, const ::dg::model::IndexRequest& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    ::grpc::ClientAsyncResponseReader< ::dg::model::IndexTxtResponse>* AsyncGetIndexTxtRaw(::grpc::ClientContext* context, const ::dg::model::IndexTxtRequest& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    const ::grpc::RpcMethod rpcmethod_Recognize_;
    const ::grpc::RpcMethod rpcmethod_BatchRecognize_;
    const ::grpc::RpcMethod rpcmethod_GetIndex_;
    const ::grpc::RpcMethod rpcmethod_GetIndexTxt_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    virtual ::grpc::Status Recognize(::grpc::ServerContext* context, const ::dg::model::WitnessRequest* request, ::dg::model::WitnessResponse* response);
    virtual ::grpc::Status BatchRecognize(::grpc::ServerContext* context, const ::dg::model::WitnessBatchRequest* request, ::dg::model::WitnessBatchResponse* response);
    virtual ::grpc::Status GetIndex(::grpc::ServerContext* context, const ::dg::model::IndexRequest* request, ::dg::model::IndexResponse* response);
    virtual ::grpc::Status GetIndexTxt(::grpc::ServerContext* context, const ::dg::model::IndexTxtRequest* request, ::dg::model::IndexTxtResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_Recognize : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_Recognize() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_Recognize() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status Recognize(::grpc::ServerContext* context, const ::dg::model::WitnessRequest* request, ::dg::model::WitnessResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestRecognize(::grpc::ServerContext* context, ::dg::model::WitnessRequest* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::WitnessResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_BatchRecognize : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_BatchRecognize() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_BatchRecognize() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status BatchRecognize(::grpc::ServerContext* context, const ::dg::model::WitnessBatchRequest* request, ::dg::model::WitnessBatchResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestBatchRecognize(::grpc::ServerContext* context, ::dg::model::WitnessBatchRequest* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::WitnessBatchResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_GetIndex : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_GetIndex() {
      ::grpc::Service::MarkMethodAsync(2);
    }
    ~WithAsyncMethod_GetIndex() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status GetIndex(::grpc::ServerContext* context, const ::dg::model::IndexRequest* request, ::dg::model::IndexResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestGetIndex(::grpc::ServerContext* context, ::dg::model::IndexRequest* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::IndexResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(2, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_GetIndexTxt : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_GetIndexTxt() {
      ::grpc::Service::MarkMethodAsync(3);
    }
    ~WithAsyncMethod_GetIndexTxt() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status GetIndexTxt(::grpc::ServerContext* context, const ::dg::model::IndexTxtRequest* request, ::dg::model::IndexTxtResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestGetIndexTxt(::grpc::ServerContext* context, ::dg::model::IndexTxtRequest* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::IndexTxtResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(3, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_Recognize<WithAsyncMethod_BatchRecognize<WithAsyncMethod_GetIndex<WithAsyncMethod_GetIndexTxt<Service > > > > AsyncService;
  template <class BaseClass>
  class WithGenericMethod_Recognize : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_Recognize() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_Recognize() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status Recognize(::grpc::ServerContext* context, const ::dg::model::WitnessRequest* request, ::dg::model::WitnessResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_BatchRecognize : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_BatchRecognize() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_BatchRecognize() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status BatchRecognize(::grpc::ServerContext* context, const ::dg::model::WitnessBatchRequest* request, ::dg::model::WitnessBatchResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_GetIndex : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_GetIndex() {
      ::grpc::Service::MarkMethodGeneric(2);
    }
    ~WithGenericMethod_GetIndex() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status GetIndex(::grpc::ServerContext* context, const ::dg::model::IndexRequest* request, ::dg::model::IndexResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_GetIndexTxt : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_GetIndexTxt() {
      ::grpc::Service::MarkMethodGeneric(3);
    }
    ~WithGenericMethod_GetIndexTxt() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status GetIndexTxt(::grpc::ServerContext* context, const ::dg::model::IndexTxtRequest* request, ::dg::model::IndexTxtResponse* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
};

}  // namespace model
}  // namespace dg


#endif  // GRPC_witness_2eproto__INCLUDED
