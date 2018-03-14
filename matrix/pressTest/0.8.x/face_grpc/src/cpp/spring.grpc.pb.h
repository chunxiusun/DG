// Generated by the gRPC protobuf plugin.
// If you make any local change, they will be lost.
// source: spring.proto
#ifndef GRPC_spring_2eproto__INCLUDED
#define GRPC_spring_2eproto__INCLUDED

#include "spring.pb.h"

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

// ## Business Intelligence APIs
class SpringService GRPC_FINAL {
 public:
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    // ### Index APIs
    virtual ::grpc::Status IndexVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::dg::model::NullMessage* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>> AsyncIndexVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>>(AsyncIndexVehicleRaw(context, request, cq));
    }
    virtual ::grpc::Status BingoVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::dg::model::NullMessage* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>> AsyncBingoVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>>(AsyncBingoVehicleRaw(context, request, cq));
    }
  private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>* AsyncIndexVehicleRaw(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::dg::model::NullMessage>* AsyncBingoVehicleRaw(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub GRPC_FINAL : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel);
    ::grpc::Status IndexVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::dg::model::NullMessage* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>> AsyncIndexVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>>(AsyncIndexVehicleRaw(context, request, cq));
    }
    ::grpc::Status BingoVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::dg::model::NullMessage* response) GRPC_OVERRIDE;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>> AsyncBingoVehicle(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>>(AsyncBingoVehicleRaw(context, request, cq));
    }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>* AsyncIndexVehicleRaw(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    ::grpc::ClientAsyncResponseReader< ::dg::model::NullMessage>* AsyncBingoVehicleRaw(::grpc::ClientContext* context, const ::dg::model::VehicleObj& request, ::grpc::CompletionQueue* cq) GRPC_OVERRIDE;
    const ::grpc::RpcMethod rpcmethod_IndexVehicle_;
    const ::grpc::RpcMethod rpcmethod_BingoVehicle_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    // ### Index APIs
    virtual ::grpc::Status IndexVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response);
    virtual ::grpc::Status BingoVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_IndexVehicle : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_IndexVehicle() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_IndexVehicle() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status IndexVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestIndexVehicle(::grpc::ServerContext* context, ::dg::model::VehicleObj* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::NullMessage>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithAsyncMethod_BingoVehicle : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithAsyncMethod_BingoVehicle() {
      ::grpc::Service::MarkMethodAsync(1);
    }
    ~WithAsyncMethod_BingoVehicle() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status BingoVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestBingoVehicle(::grpc::ServerContext* context, ::dg::model::VehicleObj* request, ::grpc::ServerAsyncResponseWriter< ::dg::model::NullMessage>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(1, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_IndexVehicle<WithAsyncMethod_BingoVehicle<Service > > AsyncService;
  template <class BaseClass>
  class WithGenericMethod_IndexVehicle : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_IndexVehicle() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_IndexVehicle() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status IndexVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithGenericMethod_BingoVehicle : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service *service) {}
   public:
    WithGenericMethod_BingoVehicle() {
      ::grpc::Service::MarkMethodGeneric(1);
    }
    ~WithGenericMethod_BingoVehicle() GRPC_OVERRIDE {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status BingoVehicle(::grpc::ServerContext* context, const ::dg::model::VehicleObj* request, ::dg::model::NullMessage* response) GRPC_FINAL GRPC_OVERRIDE {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
};

}  // namespace model
}  // namespace dg


#endif  // GRPC_spring_2eproto__INCLUDED