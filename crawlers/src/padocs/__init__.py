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
    WHERE area_name = '%s' and start_date>='%s' and start_date<='%s' LIMIT 10""" % (area, start, end)
    result = db.query(query)
    for r in result:
        context.emit(data={'url': r['url']})


def aleph_process(context, data):
    #print(data)
    """
    {'content_hash': 'b806c7328831ba0af27bf9eb67d83ef9639f214d', 'url': 'https://planning.bournemouth.gov.uk/plandisp.aspx?recno=95933&tab=2', 'title': 'Application Form - Without Personal Data', 'file_name': '\\\\dv-fileapp1\\wp\\Planning_Portal_Applications\\Planning\\7-2018-27124\\ApplicationFormNoPersonalData.pdf', 'aleph_id': '3.ac3a92c499842414a4b5f0e01bdfce478c2ec5e4', 'aleph_document': {'crawler': 'bournemouth', 'foreign_id': 'https://planning.bournemouth.gov.uk/plandisp.aspx?recno=95933&tab=2', 'source_url': 'https://planning.bournemouth.gov.uk/plandisp.aspx?recno=95933&tab=2', 'title': 'Application Form - Without Personal Data', 'file_name': '\\\\dv-fileapp1\\wp\\Planning_Portal_Applications\\Planning\\7-2018-27124\\ApplicationFormNoPersonalData.pdf', 'headers': {}, 'keywords': [], 'languages': [], 'countries': [], 'id': '3.ac3a92c499842414a4b5f0e01bdfce478c2ec5e4'}, 'aleph_collection_id': '2'}
    """
    out = {
        'source_url': data.get('url'),
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