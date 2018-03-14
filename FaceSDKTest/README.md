# how to make demo and use
cp /home/zhouping/workspace/lib/libdgface.so /usr/lib/libdgface.so
cd /home/zhouping/workspace/faceSdkTest/suite
g++ -shared -o /home/zhouping/workspace/faceSdkTest/lib/dgface_config.so -fPIC -I/usr/include/python2.7 /home/zhouping/workspace/faceSdkTest/demo/dgface_config_wrapper.cpp -lpython2.7 -lboost_python -L /usr/lib -ldgface                                    
