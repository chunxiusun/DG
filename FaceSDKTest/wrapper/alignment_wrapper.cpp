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
#include "../../../dgface_sdk/include/alignment.h"

using namespace boost::python;
using namespace std;
using namespace DGFace;
using namespace cv;

BOOST_PYTHON_MODULE(alignment)
{

    enum_<align_method>("align_method")
    .value("DLIB", align_method::DLIB)
    .value("CDNN", align_method::CDNN)
    .value("CDNN_CAFFE", align_method::CDNN_CAFFE);
    ;

    enum_<EncryptType>("EncryptType")
    .value("NON_ENCRYPT", EncryptType::NON_ENCRYPT)
    .value("DOG", EncryptType::DOG)
    .value("KMS_TENCENT", EncryptType::KMS_TENCENT);
    ;

    void (Alignment::*d1)(const std::vector<cv::Mat> &, const std::vector<cv::RotatedRect> &, std::vector<AlignResult> &, bool) = &Alignment::align;
    void (Alignment::*d2)(const cv::Mat &, const cv::RotatedRect &, AlignResult &, bool) = &Alignment::align;

    class_<Alignment, std::shared_ptr<Alignment>, boost::noncopyable>("Alignment", no_init)
        .def("align", d1)
        .def("align", d2)
        .def("is_face", &Alignment::is_face)
        .def("create_alignment", create_alignment, return_value_policy<manage_new_object>())
        .def("create_alignment_with_config", create_alignment_with_config, return_value_policy<manage_new_object>())
        .def("create_alignment_with_global_dir", create_alignment_with_global_dir, return_value_policy<manage_new_object>());
    ;


    def("create_alignment", (Alignment*(*)())create_alignment, return_value_policy<return_opaque_pointer>());
    def("create_alignment_with_config", (Alignment*(*)())create_alignment_with_config, return_value_policy<return_opaque_pointer>());
    def("create_alignment_with_global_dir", (Alignment*(*)())create_alignment_with_global_dir, return_value_policy<return_opaque_pointer>());
}	
