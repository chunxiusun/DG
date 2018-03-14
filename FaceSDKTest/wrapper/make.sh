if false; then
#alignment
g++ -std=c++11 -shared -o ../lib/alignment.so -fPIC -I/usr/include/python2.7 alignment_wrapper.cpp -lpython2.7 -lboost_python -L /usr/lib -ldgface

#detector
g++ -std=c++11 -shared -o ../lib/detector.so -fPIC -I/usr/include/python2.7 detector_wrapper.cpp -lpython2.7 -lboost_python -L /usr/lib -ldgface

#recognition
g++ -std=c++11 -shared -o ../lib/recognition.so -fPIC -I/usr/include/python2.7 recognition_wrapper.cpp -lpython2.7 -lboost_python -L /usr/lib -ldgface
fi
