CREATE TABLE customers(
	id serial PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	dob DATE NOT NULL,
	updated_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_timestamp BEFORE UPDATE
    ON customers FOR EACH ROW EXECUTE PROCEDURE 
    update_timestamp();