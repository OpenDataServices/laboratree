from urllib.parse import urljoin
from memorious.helpers.key import make_id


EXCLUDE_DOCS = ['plan', 'drawing', 'elevations', 'photograph']


def docs_url(context, data):
    # sets to 'Documents' tab
    url = data['url'].replace('activeTab=summary', 'activeTab=documents')
    context.emit(data={'url': url})


def parse(context, data):

    with context.http.rehash(data) as result:
        if result.html is not None:
            docstable = result.html.find(".//table[@id='Documents']")

            if docstable is not None:
                for row in docstable.findall(".//tr"):
                    tds = row.findall(".//td")

                    if len(tds) > 1:
                        link_i = len(tds) - 1 # Assume view link is last col
                        desc_i = len(tds) - 2 # Assume description is second to last col

                        try:
                            file = tds[link_i].find(".//a").get('href')
                            title = tds[desc_i].text or '(no title)'

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
                                context.emit_warning("Skipping document: %s [%s]" % (title, result.url))

                        except Exception as e:
                            context.emit_warning("Problem with table [%s]\n%s" % (result.url, e))

            else:
                context.emit_warning("No documents table found [%s]" % result.url)


def include_doc(title):

    for term in EXCLUDE_DOCS:
        if term in title.lower():
            return False

    return True