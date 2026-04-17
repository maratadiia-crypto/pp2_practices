CREATE OR REPLACE PROCEDURE upsert_user(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook WHERE username = p_username
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION insert_multiple_users(
    p_usernames TEXT[],
    p_phones TEXT[]
)
RETURNS TABLE (
    bad_username TEXT,
    bad_phone TEXT,
    reason TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_usernames, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        bad_username := NULL;
        bad_phone := NULL;
        reason := 'Arrays must have the same length';
        RETURN NEXT;
        RETURN;
    END IF;

    FOR i IN 1..array_length(p_usernames, 1)
    LOOP
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            IF EXISTS (
                SELECT 1 FROM phonebook WHERE username = p_usernames[i]
            ) THEN
                UPDATE phonebook
                SET phone = p_phones[i]
                WHERE username = p_usernames[i];
            ELSE
                INSERT INTO phonebook(username, phone)
                VALUES (p_usernames[i], p_phones[i]);
            END IF;
        ELSE
            bad_username := p_usernames[i];
            bad_phone := p_phones[i];
            reason := 'Invalid phone number';
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = p_value
       OR phone = p_value;
END;
$$;