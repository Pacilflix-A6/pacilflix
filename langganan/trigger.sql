CREATE OR REPLACE FUNCTION update_or_insert_transaction() RETURNS TRIGGER AS $$
DECLARE
    transaction_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM TRANSACTION
        WHERE username = NEW.username
        AND end_date_time > CURRENT_TIMESTAMP
    ) INTO transaction_exists;
    
    IF transaction_exists THEN
        UPDATE TRANSACTION
        SET end_date_time = NEW.end_date_time,
            nama_paket = NEW.nama_paket,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = CURRENT_TIMESTAMP
        WHERE username = NEW.username
        AND end_date_time > CURRENT_TIMESTAMP;
    ELSE
        INSERT INTO TRANSACTION (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
        VALUES (NEW.username, NEW.start_date_time, NEW.end_date_time, NEW.nama_paket, NEW.metode_pembayaran, CURRENT_TIMESTAMP);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER transaction_trigger
BEFORE INSERT ON TRANSACTION
FOR EACH ROW
WHEN (pg_trigger_depth() = 0)
EXECUTE FUNCTION update_or_insert_transaction();