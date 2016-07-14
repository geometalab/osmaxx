-- try casting to float and return NULL if failed
create or replace function cast_to_float_null_if_failed(v_input text) returns float as $$
begin
    return cast(v_input as float);
exception
    when invalid_text_representation then
        RAISE NOTICE 'Invalid float value: "%".  Returning NULL.', v_input;
        return NULL;
end;
$$ language plpgsql immutable;
