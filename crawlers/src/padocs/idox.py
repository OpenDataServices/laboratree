from urllib.parse import urljoin
from memorious.helpers.key import make_id


EXCLUDE_DOCS = ['plan', 'drawing', 'elevation', 'photograph']


def docs_url(context, data):
    # sets to 'Documents' tab
    url = data['url'].replace('activeTab=summary', 'activeTab=documents')
    context.emit(data={'url': url})


def parse(context, data):

    with context.http.rehash(data) as result:
        doc = parse_for_doc(result)
        if doc is not None:
            context.emit(data=doc)


def fetch_doc(context, data):
    """ Parse the PA page for the documents, then also fetch them, including cookies and referer header."""
    with context.http.rehash(data) as result:

        headers = {'Referer': result.url}

        if result.headers.get('Set-Cookie'):
            cookie = set_cookie(result.headers.get('Set-Cookie'))
            headers['Cookie'] = cookie
        else:
            context.log.info("No Set-Cookie header for [%s]" %  result.url)

        doc = parse_for_doc(result)
        if doc.get('ok'):
            data.update(doc)
            doc_result = context.http.get(doc['url'], headers=headers, lazy=True)

            if not doc_result.ok:
                err = (doc_result.url, doc_result.status_code)
                context.emit_warning("Fetch fail [%s]: HTTP %s" % err)
                if not context.params.get("emit_errors", False):
                    return
            else:
                context.log.info("Fetched [%s]: %r", doc_result.status_code, doc_result.url)
                data.update(doc_result.serialize())
                context.emit(data=data)

        elif doc.get('warn'):
            context.emit_warning(doc.get('warn'))
        elif doc.get('info'):
            context.log.info(doc.get('info'))


def parse_for_doc(result):

    doc = {'ok': False}

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
                                'ok': True,
                                'url': url,
                                'source_url': result.url,
                                'file_name': file,
                                'title': title,
                                'request_id': make_id(url)
                            }

                            return doc

                        else:
                            doc['info'] = "Skipping document: %s [%s]" % (title, result.url)

                    except Exception as e:
                        doc['warn'] = "Problem with table [%s]\n%s" % (result.url, e)

        else:
            doc['warn'] = "No documents table found [%s]" % result.url

    else:
        doc['warn'] = "Bad response [%s] % result.url"

    return doc


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
    elif doctype is not None and doctype != '':
        return doctype.strip()
    else:
        return '(no title)'



def include_doc(title):

    for term in EXCLUDE_DOCS:
        if term in title.lower():
            return False

    return True



def set_cookie(set_cookie_header):
    cookies = [c.strip() for c in set_cookie_header.replace(',',';').split(';') if 'JSESSIONID' in c]
    return '; '.join(cookies)