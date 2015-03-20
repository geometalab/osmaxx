import os

APPLICATION_SETTINGS = {
    'data_directory': os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '../data/')),
    'download_file_name': '%(id)s-%(name)s',
    'dowload_chunk_size': 8192
}
