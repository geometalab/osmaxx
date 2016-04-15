**svg to ttf automated conversion process**

-	Clone pysvg2font module from [carrasti/pysvg2font](https://github.com/carrasti/pysvg2font.git)
-	Generate the ttf file as instructed on the documentation of the repository
-	You can recheck the result of the generated font using [fontforge](https://fontforge.github.io/en-US/).


Throughout the process, error 
	`Failed to parse colour` 
will be generated. However, this error can be safely neglected.

pysvg2font module was modified to result alphabetically ordered font.
from `pysvg2font/pysvg2font/__init__.py` line 94:

	`file_path.sort()`




