-- create postgresql database and user for development environment
REASSIGN OWNED BY test_dev TO postgres;
DROP OWNED BY test_dev;
DROP USER IF EXISTS test_dev;
DROP DATABASE IF EXISTS testing_db;

CREATE USER test_dev WITH password 'test_dev_pwd' CREATEDB CREATEROLE;
CREATE DATABASE testing_db
	TEMPLATE template0
	OWNER test_dev
	ENCODING 'utf8'
	LC_COLLATE 'en_US.utf8'
	LC_CTYPE 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE testing_db to test_dev;
GRANT USAGE, CREATE ON SCHEMA public TO test_dev;
