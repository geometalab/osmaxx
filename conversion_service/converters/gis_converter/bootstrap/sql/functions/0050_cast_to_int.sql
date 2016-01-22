-- try casting to int and return NULL if failed
create or replace function cast_to_int_null_if_failed(text, integer) returns integer as $$
begin
    return cast($1 as int);
exception
    when invalid_text_representation then
        return NULL;
end;
$$ language plpgsql immutable;