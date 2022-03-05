pre-build:
	pip install --upgrade pip && \
	pip install -r requirements.txt

test-unit:
	@echo "[Mocking] Running unit tests for the API..."
