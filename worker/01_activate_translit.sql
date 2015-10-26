CREATE FUNCTION transliterate(text) RETURNS text AS '$libdir/utf8translit', 'transliterate' LANGUAGE C STRICT;
