import os
import zipfile


def check_if_result_contains_data(binary_data, assert_greater):
    FILE_NAME = 'file.zip'
    file = open(FILE_NAME, mode='wb')
    file.write(binary_data)
    file.flush()
    file.close()
    with zipfile.ZipFile(FILE_NAME, 'r') as zip_file:
        for zip_info in zip_file.filelist:
            endings = (
                '.dbf',
                '.shp',
                '.shx',
                '.prj',
                '.gpkg',
                '.csv',
                '.txt',
                'pdf',
                '.odt',
                'sqlite',
            )
            if zip_info.filename.endswith(endings):
                assert_greater(zip_info.file_size, 80)
    os.unlink(FILE_NAME)
