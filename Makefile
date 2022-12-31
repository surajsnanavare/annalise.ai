include .env
export

verbosity=1

help:
	@echo "Usage:"
	@echo " make help			-- display this help"
	@echo " make Install			-- creates database, install dependancies and migrates migrations"
	@echo " make run			-- run server"
	@echo " make test			-- run the tests and checks lint issues"
	@echo " make install-django		-- migrates migrations"
	@echo " make install-pip		-- install dependancies"


# Install dependancies and run migrations
install: install-pip install-django

# Install all required dependencies
install-pip:
	@pip install -r requirements.txt

# Run migration on database
install-django:
	@python manage.py collectstatic  --no-input
	@python manage.py migrate

# Start application
run:
	@python manage.py runserver 0.0.0.0:${PORT}

# Run tests
test:
	@coverage run  --source=$(path) manage.py test --keepdb --verbosity=$(verbosity) $(path)
	@coverage report -m
