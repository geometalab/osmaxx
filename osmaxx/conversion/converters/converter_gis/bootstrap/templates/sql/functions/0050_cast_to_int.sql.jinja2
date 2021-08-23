-- try casting to int and return NULL if failed
create or replace function cast_to_int_null_if_failed(v_input text) returns integer as $$
begin
    return cast(v_input as int);
exception
    when invalid_text_representation then
        RAISE NOTICE 'Invalid integer value: "%".  Returning NULL.', v_input;
        return NULL;
end;
$$ language plpgsql immutable;
