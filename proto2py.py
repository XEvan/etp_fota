import os

os.system("python -m grpc_tools.protoc -I=./protos --python_out=./rpc_package --grpc_python_out=./rpc_package ./protos/callinvoker.proto")