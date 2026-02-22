.PHONY: validate schema-check prompt-check cli-help compare-lab01 benchmark-normalize

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

benchmark-normalize:
	./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP
