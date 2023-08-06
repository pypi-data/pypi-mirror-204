import datetime


def db_model_to_dict(model, firstcol=None):
    """
    Convert SQLAlchemy model to a dictionary with its column names as keys
    """
    data = {}
    if firstcol:
        data[firstcol] = ''
        data['name'] = model.name
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.isoformat()
        data[column.name] = value
    return data


def image_rotate(imagename: str, rotateDegree: int):
    from PIL import Image
    # Giving The Original image Directory
    Original_Image = Image.open(imagename)
    rotated_image1 = Original_Image.transpose(Image.ROTATE_90)
    rotated_image1.save(imagename)


def safe_naming(name):
    keepcharacters = ('.', '_')
    return "".join(c for c in name if c.isalnum() or c in keepcharacters).rstrip()
