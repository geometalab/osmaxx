-- try casting to float and return NULL if failed
CREATE OR REPLACE FUNCTION cast_to_float_null_if_failed(v_input text) RETURNS FLOAT AS $$
BEGIN
    RETURN CAST(v_input AS FLOAT);
EXCEPTION
    WHEN invalid_text_representation THEN
        RAISE NOTICE 'Invalid float value: "%".  Returning NULL.', v_input;
        RETURN NULL;
END;
$$ LANGUAGE PLPGSQL IMMUTABLE;
