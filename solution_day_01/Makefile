
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y luxury || :
	@pip install -e .

run_preprocess:
	python -c 'from luxury.interface.main_local import preprocess_and_train; preprocess_and_train()'


##################### CLEANING #####################

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr **/__pycache__ **/*.pyc
	@rm -fr **/build **/dist
	@rm -fr proj-*.dist-info
	@rm -fr proj.egg-info
	@rm -f **/.DS_Store
	@rm -f **/*Zone.Identifier
	@rm -f **/.ipynb_checkpoints
