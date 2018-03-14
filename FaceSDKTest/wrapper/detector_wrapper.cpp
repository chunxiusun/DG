//#include <Python.h>
#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/list.hpp>
#include <boost/python/object.hpp>
#include <boost/python/wrapper.hpp>
#include <boost/python/enum.hpp>
#include <boost/python.hpp>

#include "../../../dgface_sdk/include/detector.h"

using namespace boost::python;
using namespace std;
using namespace DGFace;


struct DetectorWrapper : Detector, wrapper<Detector>
{
    virtual bool set_minface(int min_face_size)
    {
        if (override n = this->get_override("set_minface"))
            return n(min_face_size);
        return Detector::set_minface(min_face_size);
    }
    virtual bool default_set_minface(int min_face_size)
    {
        return this->Detector::set_minface(min_face_size);
    }

    virtual bool set_maxface(int max_face_size)
    {
        if (override n = this->get_override("set_maxface"))
            return n(max_face_size);
        return Detector::set_maxface(max_face_size);
    }
    virtual bool default_set_maxface(int max_face_size)
    {
        return this->Detector::set_maxface(max_face_size);
    }
};

BOOST_PYTHON_MODULE(detector)
{
    using namespace std;
    using namespace boost::python;
    using namespace DGFace;

    enum_<det_method>("det_method")
    .value("DLIB", det_method::DLIB)
    .value("SSD", det_method::SSD)
    .value("RPN", det_method::RPN)
    .value("FCN", det_method::FCN)    
    .value("RFCN", det_method::RFCN);
    ;

    enum_<EncryptType>("EncryptType")
    .value("NON_ENCRYPT", EncryptType::NON_ENCRYPT)
    .value("DOG", EncryptType::DOG)
    .value("KMS_TENCENT", EncryptType::KMS_TENCENT);
    ;

//    namespace python = boost::python;
//    python::enum_<TestClass::det_method>("det_method")
//    .value("DLIB", TestClass::DLIB)
//    .value("SSD", TestClass::SSD)
//    .value("RPN", TestClass::RPN)
//    .value("FCN", TestClass::FCN)    
//    .value("RFCN", TestClass::RFCN);
//    ;

    class_<DetectorWrapper, std::shared_ptr<DetectorWrapper>, boost::noncopyable>("Detector", no_init)
      .def("detect", &Detector::detect)
      .def("set_minface", &Detector::set_minface, &DetectorWrapper::default_set_minface)
      .def("set_maxface", &Detector::set_maxface, &DetectorWrapper::default_set_maxface)
      .def("get_detect_face_info",&Detector::get_detect_face_info)
      .def("create_detector", create_detector, return_value_policy<manage_new_object>())
      .def("create_detector_with_config", create_detector_with_config, return_value_policy<return_opaque_pointer>())
      .def("create_detector_with_global_dir", create_detector_with_global_dir, return_value_policy<return_opaque_pointer>())
    ;

//    def("createDetectorInstance", Detector::Detector, return_value_policy<manage_new_object>());
    def("create_detector", (Detector*(*)())create_detector, return_value_policy<manage_new_object>());
    def("create_detector_with_config", (Detector*(*)())create_detector_with_config, return_value_policy<manage_new_object>());
    def("create_detector_with_global_dir", (Detector*(*)())create_detector_with_global_dir, return_value_policy<manage_new_object>());
}


/*
struct DetectorWrap : Detector, wrapper<Detector>
{
    public:

    bool set_minface(int min_face_size)
    {
        this->get_override("set_minface")(min_face_size);
    }
    bool set_maxface(int max_face_size)
    {
        this->get_override("set_maxface")(max_face_size);
    }
};


BOOST_PYTHON_MODULE(detector)
{
    using namespace std;
    using namespace boost::python;
    using namespace DGFace;

    class_<DetectorWrap, boost::noncopyable>("Detector", no_init)
      .def("set_minface", boost::python::pure_virtual(&Detector::set_minface))
      .def("set_maxface", boost::python::pure_virtual(&Detector::set_maxface))
      .def("get_detect_face_info",&Detector::get_detect_face_info)
      .def("create_detector", create_detector)
      .def("create_detector_with_config", create_detector_with_config)
      .def("create_detector_with_global_dir", create_detector_with_global_dir);
      ;


    def("create_detector", create_detector);
    def("create_detector_with_config", create_detector_with_config);
    def("create_detector_with_global_dir", create_detector_with_global_dir);
}
*/
