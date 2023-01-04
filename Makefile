PORT ?= 8000
SCRIPT="./pychat/database.py"

.PHONY: start

start:
	uvicorn pychat.main:app --host 0.0.0.0 --port ${PORT}

start_debug:
	uvicorn pychat.main:app --host 0.0.0.0 --port ${PORT} --reload

upgrade:
	@echo "Attempting to upgrade db..."
	python ${SCRIPT} "upgrade"

downgrade:
	@echo "Attempting to downgrade db..."
	python ${SCRIPT} "downgrade"

makemigrations:
	@echo "Attempting to generate db migrations..."
	python ${SCRIPT} "makemigrations"

init:
	@echo "Attempting to initialize db..."
	python ${SCRIPT} "init"

echo:
	@echo ${PORT}
