CFN_TEMPLATES=$(wildcard *.yml */*.yml */*/*.yml)

.PHONY: python-test-step1 python-test-step2 python-test-step3 python-test-final python-build deploy-macro deploy-s3 deploy-vpc cfn-lint goto-step1 goto-step2 goto-step3 goto-step4 goto-finished
python-test-step1:
	@python3 python/step1/test.py
python-test-step2:
	@python3 python/step2/test.py
python-test-step3:
	@python3 python/step3/test.py
python-test-step4:
	@python3 python/step4/test.py
python-test-final:
	@python3 python/finished/test.py

node-test-step1:
	@mocha test node/step1/test
node-test-step2:
	@mocha test node/step2/test
node-test-step3:
	@mocha test node/step3/test
node-test-step4:
	@mocha test node/step4/test
node-test-final:
	@mocha test node/finished/test

python-build:
# TODO fix hardcoded bucket
	@aws cloudformation package --template-file ./python/finished/macro-template.yml --s3-bucket lambda-artefacts-bucket-1dd4wu1p9m98k --output-template-file packaged-macro.yml

node-build:
	@aws cloudformation package --template-file ./node/finished/macro-template.yml --s3-bucket lambda-artefacts-bucket-1dd4wu1p9m98k --output-template-file packaged-macro.yml

deploy-macro:
	@aws cloudformation deploy --template-file ./packaged-macro.yml --stack-name Macro-NaclExpander --capabilities CAPABILITY_IAM

deploy-s3:
	@aws cloudformation deploy --template-file ./s3.yml --stack-name macro-workshop-artefacts

deploy-vpc:
	@aws cloudformation deploy --template-file ./test-vpc.yml --stack-name macro-test-vpc

cfn-lint:
	@$(foreach template,$(CFN_TEMPLATES),(echo "Running cfn-lint on $(template)" && cfn-lint  --ignore-checks W3002  --override-spec cfn-lint/override-file.json $(template))  || exit $$?;)

goto-step1:
	@git checkout step1
goto-step2:
	@git checkout step2
goto-step3:
	@git checkout step3
goto-step4:
	@git checkout step4
goto-finished:
	@git checkout finished