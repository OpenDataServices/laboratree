from urllib.parse import urljoin
from memorious.helpers.key import make_id


EXCLUDE_DOCS = ['plan', 'drawing', 'elevation', 'photograph']


def docs_url(context, data):
    # sets to 'Documents' tab
    url = data['url'].replace('activeTab=summary', 'activeTab=documents')
    context.emit(data={'url': url})


def parse(context, data):

    with context.http.rehash(data) as result:
        if result.html is not None:
            docstable = result.html.find(".//table[@id='Documents']")

            if docstable is not None:
                ths = docstable.findall(".//th")
                docs_i = get_document_indices(ths)

                for row in docstable.findall(".//tr"):

                    tds = row.findall(".//td")
                    if len(tds) > 0:

                        try:
                            file = tds[docs_i['view']].find(".//a").get('href')
                            title = get_document_title(tds, docs_i)

                            if include_doc(title):

                                url = urljoin(result.url, file)
                                doc = {
                                    'url': url,
                                    'source_url': result.url,
                                    'file_name': file,
                                    'title': title,
                                    'request_id': make_id(url)
                                }

                                context.emit(data=doc)

                            else:
                                context.log.info("Skipping document: %s [%s]" % (title, result.url))

                        except Exception as e:
                            context.emit_warning("Problem with table [%s]\n%s" % (result.url, e))

            else:
                context.emit_warning("No documents table found [%s]" % result.url)


def get_document_indices(ths):

    headings = ['view', 'description', 'type']
    indices = {}
    for i, th in enumerate(ths):
        for h in headings:
            try:
                th_h = th.text_content().strip().lower()
            except AttributeError:
                th_h = ''
            if h in th_h:
                indices[h] = i

    return indices


def get_document_title(tds, docs_i):
    desc = tds[docs_i['description']].text
    doctype = tds[docs_i['type']].text
    if desc is not None and desc != '':
        return desc.strip()
    elif doctype is not None and doctype is not '':
        return doctype.strip()
    else:
        return '(no title)'



def include_doc(title):

    for term in EXCLUDE_DOCS:
        if term in title.lower():
            return False

    return True