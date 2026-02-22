.PHONY: validate schema-check prompt-check cli-help compare-lab01 cli-smoke ci-check \
	benchmark-normalize doctor bringup-lab01 check-lab01 teardown-lab01

validate: schema-check prompt-check

schema-check:
	python3 -m unittest discover -s tests -v

prompt-check:
	@test -f .prompts/PROMPT_00_s.txt
	@test -f .prompts/PROMPT_01_s.txt
	@test -f .prompts/PROMPT_02_s.txt
	@test -f .prompts/PROMPT_03_s.txt
	@test -f .prompts/PROMPT_04_s.txt
	@test -f .prompts/PROMPT_05_s.txt
	@test -f .prompts/PROMPT_06_s.txt

cli-help:
	./cli-tools/mobile-systems-lab --help

compare-lab01:
	./cli-tools/mobile-systems-lab compare LAB_01_SENSOR_TOGGLE_APP

cli-smoke: cli-help compare-lab01

ci-check: validate cli-smoke

benchmark-normalize:
	./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP

doctor:
	bash scripts/dev/doctor.sh

bringup-lab01:
	bash scripts/dev/bringup_lab01.sh

check-lab01:
	bash scripts/dev/check_lab01.sh

teardown-lab01:
	bash scripts/dev/teardown_lab01.sh
