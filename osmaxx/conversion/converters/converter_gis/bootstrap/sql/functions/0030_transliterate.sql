---------------------------------------------------------------------------------------
-- write or print (a letter or word) using the closest corresponding letters of
-- a different alphabet or language.
-- EG. select osml10n_translit('Москва́');
--     Moskvá
---------------------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS postgis CASCADE;
CREATE EXTENSION IF NOT EXISTS osml10n CASCADE;
