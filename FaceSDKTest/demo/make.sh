#export CPLUS_INCLUDE_PATH=/home/zhouping/dgface_sdk/include:$CPLUS_INCLUDE_PATH
#g++ -shared -o dgface_config.so -fPIC -I/usr/include/python2.7 dgface_config_wrapper.cpp -lpython2.7 -lboost_python  libdgface.so 
#g++ -shared -o dgface_config.so -fPIC -I/usr/include/python2.7 dgface_config_wrapper.cpp -lpython2.7 -lboost_python -ldgface
g++ -shared -o lib/dgface_config.so -fPIC -I/usr/include/python2.7 dgface_config_wrapper.cpp -lpython2.7 -lboost_python -L /usr/lib -ldgface
