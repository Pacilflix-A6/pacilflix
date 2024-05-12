CREATE OR REPLACE FUNCTION check_username_exists() RETURNS TRIGGER AS
$$
DECLARE
username_exists BOOLEAN;
BEGIN
SELECT EXISTS(
SELECT 1
FROM pengguna
WHERE username = NEW.username
) INTO username_exists;
IF username_exists THEN
RAISE EXCEPTION 'Username % already exists', NEW.username;
END IF;
RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER prevent_identical_username
BEFORE INSERT ON pengguna
FOR EACH ROW
EXECUTE FUNCTION check_username_exists();