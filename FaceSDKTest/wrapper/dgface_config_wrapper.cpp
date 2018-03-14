#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <Python.h>
#include <boost/python/class.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/list.hpp>
#include <boost/python/object.hpp>

#include "../../dgface_sdk/include/dgface_config.h"

BOOST_PYTHON_MODULE(dgface_config){   

    using namespace std;
    using namespace boost::python;
    using namespace DGFace;
  
    class_<Config>("Config",init<>())   
      .def("Load",&Config::Load)
      .def("LoadString",&Config::LoadString)
      .def("KeyExist",&Config::KeyExist)
      .def("AddEntry",&Config::AddEntry)
      .def("LoadString",&Config::LoadString)
      .def("getArray",&Config::getArray)
      .def("getFloatArray",&Config::getFloatArray)
      .def("getIntArray",&Config::getIntArray)
      .def("getStringArray",&Config::getStringArray)
      .def("getFloat",&Config::getFloat)
      .def("getInteger",&Config::getInteger)
      .def("getString",&Config::getString)
      .def("DumpValues",&Config::DumpValues)
      .def("Clear",&Config::Clear)
      ;   
}  
