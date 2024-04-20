.PHONY: tests
tests:
	cd $(collection) && MOLECULE_PLATFORM_IMAGE=debian12-systemd molecule test --all
	cd $(collection) && MOLECULE_PLATFORM_IMAGE=alma9-systemd molecule test --all
	cd $(collection) && MOLECULE_PLATFORM_IMAGE=amazon2023-systemd molecule test --all

.PHONY: test
test:
	cd $(collection) && MOLECULE_PLATFORM_IMAGE=$(platform) molecule test --all

.PHONY: lint
lint: yamllint ansiblelint flake8

.PHONY: yamllint
yamllint:
	yamllint .

.PHONY: ansiblelint
ansiblelint:
	ansible-lint -p *

.PHONY: flake8
flake8:
	flake8 .

.PHONY: clean
clean:
	find . -type d -name __pycache__ | xargs rm -rf {}
