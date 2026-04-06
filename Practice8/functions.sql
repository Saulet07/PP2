CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.name, c.phone FROM contacts c
                 WHERE c.name ILIKE '%' || p || '%'
                    OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.phone
    FROM contacts c
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;