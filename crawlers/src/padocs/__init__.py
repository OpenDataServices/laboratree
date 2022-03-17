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
        url = '%s&tab=2' % r['url'] # sets to 'Associated Documents' tab
        context.emit(data={'url': url})


def test(context, data):
    print(data)