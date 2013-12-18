PROTOS = rh.proto rh_config.proto
PROTOC_OPT = --python_out=.

PROTOPY = rh_pb2.py rh_config_pb2.py

all: $(PROTOPY)

rh_pb2.py: rh.proto
	protoc $(PROTOC_OPT) rh.proto

rh_config_pb2.py: rh_config.proto
	protoc $(PROTOC_OPT) rh_config.proto

clean:
	rm -f $(PROTOPY)
