import shutil
import os


class changed_dir:  # pragma: nocover # noqa  -> disable=N801
    """
    Changes into a arbitrary directory, switching back to the directory after execution of the with statement.

    directory:
        the directory that should be changed into.
    create_if_not_exists:
        set this to False, if the chgdir should fail loudly. If set to `True`,
        tries to create the directory if it doesn't exist

    fallback_to_tempdir_as_last_resort:
        assumes create_if_not_exists is also True
        creates a tmp directory as last resort, and does work there. Defaults to False.
    """

    def __init__(self, directory, create_if_not_exists=True):
        self.old_dir = os.getcwd()
        self.new_dir = directory
        self.success = None
        self.create_if_not_exists = create_if_not_exists

    def __enter__(self):
        try:
            try:
                # see if we can enter the directory
                os.chdir(self.new_dir)
                self.success = True
            except OSError:
                if self.create_if_not_exists:
                    try:
                        # see if we can create it
                        os.mkdir(self.new_dir)
                        os.chdir(self.new_dir)
                        self.success = True
                    except OSError:
                        raise
                else:
                    raise
        finally:
            return self

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_dir)
        try:
            if not self.success:
                shutil.rmtree(self.new_dir)
        except:
            pass
        return isinstance(value, OSError)
