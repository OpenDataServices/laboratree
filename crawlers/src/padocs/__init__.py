import os
import dataset


def seed_url(context, data):
    """
    Queries EPDS database.
    Expects context params:
     - start
     - end
     - area
    """
    start = context.get('start')
    end = context.get('end')
    area = context.get('area')

    db = dataset.connect(os.environ.get('EPDS_DB_URL'))
    query = """SELECT url FROM planit_key_fields
    WHERE area_name = '%s' and start_date>='%s' and start_date<='%s'""" % (area, start, end)
    result = db.query(query)
    for r in result:
        context.emit(data={'url': r['url']})


def aleph_process(context, data):

    out = {
        'source_url': data.get('source_url', data.get('url')),
        'area_name': context.crawler.name,
        'document_title': data.get('title', ''),
        'document_file_name': data.get('file_name'),
        'aleph_document_id': data.get('aleph_id'),
        'aleph_collection_id': data.get('aleph_collection_id')
    }
    context.emit(data=out)


def export(context, params):
    pass


def dump(context, data):
    print(data)