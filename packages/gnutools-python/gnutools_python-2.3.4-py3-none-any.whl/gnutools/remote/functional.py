import os
import zipfile

from gnutools import fs


def gdrive(gdrive_uri, output_dir=None):
    assert gdrive_uri.startswith("gdrive://")
    gdrive_id = gdrive_uri.split("gdrive://")[1]
    output_dir_temp = f"/tmp/.{gdrive_id}/"
    os.system(f"gdown {gdrive_id} -O {output_dir_temp}")
    assert os.path.exists(output_dir_temp)
    archive = fs.listfiles(output_dir_temp)[0]
    output_dir = f"/tmp/{gdrive_id}/"
    try:
        with zipfile.ZipFile(archive, "r") as zObject:
            zObject.extractall(output_dir)
        os.system(f"rm -r {output_dir_temp}")
    except zipfile.BadZipFile:
        os.makedirs(output_dir)
        os.system(f"mv {archive} {output_dir}")
    return fs.listfiles(output_dir)


gdrivezip = gdrive
