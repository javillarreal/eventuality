import os

from werkzeug.utils import secure_filename

from project import settings


def _get_media_propeties(context: str = 'media') -> dict:
    return settings.static_files[context.upper()]


def allowed_file(filename, context: str = 'media'):
    try
        ALLOWED_EXTENSIONS = _get_media_propeties(context)['ALLOWED_EXTENSIONS']
    except KeyError:
        return False
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file=None):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        try
            folder = _get_media_propeties(context)['FOLDER']
        except KeyError:
            return None
        
        file.save(os.path.join(folder, filename))

        return file
