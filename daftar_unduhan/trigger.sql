CREATE FUNCTION delete_download_trigger_func() RETURNS TRIGGER AS $$
BEGIN
    IF (CURRENT_TIMESTAMP - OLD.timestamp) > INTERVAL '1 day' THEN
        RETURN OLD; 
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_download_trig
BEFORE DELETE ON TAYANGAN_TERUNDUH
FOR EACH ROW
EXECUTE FUNCTION delete_download_trigger_func();