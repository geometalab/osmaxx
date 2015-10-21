# with statements are use as if they were function, so let's return it as if it was one
from utils.directory_changer_helper import ChDirWith

chg_dir_with = ChDirWith

__all__ = [
    'chg_dir_with',
]