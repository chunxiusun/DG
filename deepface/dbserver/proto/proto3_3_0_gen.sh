#!/bin/bash

makesure_dir_exist(){
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
    fi
}


if [ -z "$1" ]; then
    echo "Usage: proto_gen.sh cpp|python|golang|csharp"
    exit
fi

if [ "$1" == "cpp" ]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$3
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$5
    protoc_exe="$2/protoc"
    grpc_exe="$4/grpc_cpp_plugin"
    target="--cpp_out"
    target_dir="../src/cpp"
    makesure_dir_exist $target_dir
    $protoc_exe -I . $target=$target_dir *.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe common.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe witness.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe ranker.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe system.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe skynet.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe matrix.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe spring.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe localcommon.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe dataservice.proto
    $protoc_exe -I . --grpc_out=$target_dir --plugin=protoc-gen-grpc=$grpc_exe deepdatasingle.proto
elif [ "$1" == "python" ]; then
    grpc_x_plugin=`which grpc_python_plugin`
    target="--python_out"
    target_dir="../src/python"
    makesure_dir_exist $target_dir
    python -m grpc.tools.protoc -I . --python_out=$target_dir --grpc_python_out=$target_dir *.proto
elif [ "$1" == "golang" ]; then
    target="--go_out"
    target_dir="../src/golang"
    makesure_dir_exist $target_dir
    protoc -I . $target=$target_dir common.proto
    protoc -I . $target=$target_dir localcommon.proto
    protoc ranker.proto $target=plugins=grpc:$target_dir
    protoc witness.proto $target=plugins=grpc:$target_dir
    protoc system.proto $target=plugins=grpc:$target_dir
elif [ "$1" == "csharp" ]; then
    grpc_x_plugin=`which grpc_csharp_plugin`
    target="--csharp_out"
    target_dir="../src/csharp"
    makesure_dir_exist $target_dir

    protoc -I . --csharp_out=$target_dir --grpc_out=$target_dir *.proto --plugin=protoc-gen-grpc=$grpc_x_plugin
else
    echo "Usage: proto_gen.sh [cpp|python|golang|csharp]"
    exit
fi

echo "proto src file generated finished"




#generate grpc codes



