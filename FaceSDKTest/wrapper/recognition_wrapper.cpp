//#include <Python.h>
#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/list.hpp>
#include <boost/python/object.hpp>
#include <boost/python/wrapper.hpp>
#include <boost/python/enum.hpp>
#include <boost/python.hpp>
#include "../../../dgface_sdk/include/recognition.h"

using namespace boost::python;
using namespace std;
using namespace DGFace;
using namespace cv;

struct RecognitionWrapper : Recognition, wrapper<Recognition>
{
    virtual void recog(const std::vector<cv::Mat> &faces, std::vector<RecogResult> &results, const std::string &pre_process = "None", const bool &L2_reg = false)
    {
        if (override n = this->get_override("recog"))
            return n(faces, results, pre_process, L2_reg);
        return Recognition::recog(faces, results, pre_process, L2_reg);
    }
    virtual void default_recog(const std::vector<cv::Mat> &faces, std::vector<RecogResult> &results, const std::string &pre_process = "None", const bool &L2_reg = false)
    {
        return this->Recognition::recog(faces, results, pre_process, L2_reg);
    }

    virtual void recog(const cv::Mat &img, const cv::RotatedRect& rot_bbox, AlignResult &result, bool adjust = true)
    {
        if (override n = this->get_override("recog"))
            return n(img, rot_bbox, result, adjust);
        return Recognition::recog(img, rot_bbox, result, adjust);
    }
    virtual void default_recog(const cv::Mat &img, const cv::RotatedRect& rot_bbox, AlignResult &result, bool adjust = true)
    {
        return this->Recognition::recog(img, rot_bbox, result, adjust);
    }
};

BOOST_PYTHON_MODULE(detector)
{
    using namespace std;
    using namespace boost::python;
    using namespace DGFace;

    enum_<recog_method>("recog_method")
    .value("LBP", recog_method::LBP)
    .value("CNN", recog_method::CNN)
    .value("CDNN",recog_method::CDNN)
    .value("CDNN_CAFFE", recog_method::CDNN_CAFFE)    
    .value("CDNN_CAFFE_CROP224", recog_method::CDNN_CAFFE_CROP224)
    .value("FUSION",recog_method::FUSION)
    .value("GPU_FUSION", recog_method::GPU_FUSION);
    ;

    enum_<EncryptType>("EncryptType")
    .value("NON_ENCRYPT", EncryptType::NON_ENCRYPT)
    .value("DOG", EncryptType::DOG)
    .value("KMS_TENCENT", EncryptType::KMS_TENCENT);
    ;

    void (Recognition::*d1)(const std::vector<cv::Mat> &, std::vector<RecogResult> &, const std::string &, const bool &) = &Recognition::recog;
    void (Recognition::*d2)(const cv::Mat &, const cv::RotatedRect& , AlignResult &, bool) = &Recognition::recog;


    class_<RecognitionWrapper, std::shared_ptr<RecognitionWrapper>, boost::noncopyable>("Recognition", init<EncryptType>())
      .def("recog", &Recognition::d1, &RecognitionWrapper::default_recog)
      .def("recog", &Recognition::d2, &RecognitionWrapper::default_recog)
      .def("create_recognition", create_recognition, return_value_policy<manage_new_object>())
      .def("create_recognition_with_config", create_recognition_with_config, return_value_policy<return_opaque_pointer>())
      .def("create_recognition_with_global_dir", create_recognition_with_global_dir, return_value_policy<return_opaque_pointer>())
    ;

    .def("create_recognition", (Recognition*(*)())create_recognition, return_value_policy<manage_new_object>())
    .def("create_recognition_with_config", (Recognition*(*)())create_recognition_with_config, return_value_policy<return_opaque_pointer>())
    .def("create_recognition_with_global_dir", (Recognition*(*)())create_recognition_with_global_dir, return_value_policy<return_opaque_pointer>())
}
