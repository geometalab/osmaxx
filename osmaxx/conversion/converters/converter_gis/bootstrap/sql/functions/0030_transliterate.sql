---------------------------------------------------------------------------------------
-- write or print (a letter or word) using the closest corresponding letters of
-- a different alphabet or language.
-- EG. select transliterate('Москва́');
--     Moskvá
---------------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION transliterate(text) RETURNS text AS '$libdir/utf8translit', 'transliterate' LANGUAGE C STRICT;
