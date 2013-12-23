PROTOS = rh.proto rh_config.proto
PROTOC_OPT = --python_out=.

all: protos

protos: $(PROTOS)
	protoc $(PROTOC_OPT) $(PROTOS)

clean:
	rm -f dummy *_pb2.py *.pyc *.py~

test: protos
	python test/relays_test.py
