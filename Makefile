sys_deps:
ifeq (, $(shell which acarsdec 2> /dev/null))
	$(error Please install acarsdec, first.)
endif
ifneq (0, $(shell cat /sys/module/usbcore/parameters/usbfs_memory_mb))
	echo 0 | sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb
endif

deps:
	pip install -r requirements.txt

deps_dev:
	pip install -r requirements_dev.txt

listener:
	PYTHONPATH=. acarsserver/cli/listener.py

client: sys_deps
	PYTHONPATH=. acarsserver/cli/client.py

client_fake: clean
	PYTHONPATH=. acarsserver/cli/client_fake.py

web:
	./run.py

db_migrate:
	yoyo apply

clean:
	find . -name *.pyc -delete
	find . -name __pycache__ -type d -delete
