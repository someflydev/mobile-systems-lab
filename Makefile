.PHONY: validate schema-check prompt-check cli-help compare-lab01 cli-smoke ci-check \
	benchmark-fixtures-lab01 benchmark-normalize benchmark-regress-lab01 \
	doctor bringup-lab01 check-lab01 teardown-lab01

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

benchmark-fixtures-lab01:
	python3 cli-tools/benchmark_collect.py --lab-id LAB_01_SENSOR_TOGGLE_APP --platform kotlin_android --input artifacts/benchmark/fixtures/android --out artifacts/benchmark/results/kotlin_android/LAB_01_SENSOR_TOGGLE_APP/fixture.BENCHMARK_RESULT.json
	python3 cli-tools/benchmark_collect.py --lab-id LAB_01_SENSOR_TOGGLE_APP --platform swift_ios --input artifacts/benchmark/fixtures/ios --out artifacts/benchmark/results/swift_ios/LAB_01_SENSOR_TOGGLE_APP/fixture.BENCHMARK_RESULT.json
	python3 cli-tools/benchmark_collect.py --lab-id LAB_01_SENSOR_TOGGLE_APP --platform flutter --input artifacts/benchmark/fixtures/flutter --out artifacts/benchmark/results/flutter/LAB_01_SENSOR_TOGGLE_APP/fixture.BENCHMARK_RESULT.json
	python3 cli-tools/benchmark_collect.py --lab-id LAB_01_SENSOR_TOGGLE_APP --platform react_native --input artifacts/benchmark/fixtures/react_native --out artifacts/benchmark/results/react_native/LAB_01_SENSOR_TOGGLE_APP/fixture.BENCHMARK_RESULT.json

benchmark-normalize: benchmark-fixtures-lab01
	./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP

benchmark-regress-lab01:
	./cli-tools/mobile-systems-lab benchmark-regress LAB_01_SENSOR_TOGGLE_APP

doctor:
	bash scripts/dev/doctor.sh

bringup-lab01:
	bash scripts/dev/bringup_lab01.sh

check-lab01:
	bash scripts/dev/check_lab01.sh

teardown-lab01:
	bash scripts/dev/teardown_lab01.sh
