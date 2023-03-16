.PHONY: test-python
test-python:  ## Run python tests
	pytest ./tests/test_todo.py
	sh test.sh
	@echo "~~~ Ran python tests ~~~"
