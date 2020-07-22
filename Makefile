init:
	@pip install -r requirements.txt
	@./setup_env.sh

test:
	@python tests/*.py

run:
	@python timo/core.py run --test_name=$(test)

parse:
	@python timo/core.py parse --test_name=$(test)

insert:
	@python timo/core.py parse --test_name=$(test) --db=$(db) --build_number=$(build_number)
