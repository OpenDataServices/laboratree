from urllib.parse import urljoin
from memorious.helpers.key import make_id


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
                    if len(tds) > 0:
                        # 0: checkbox, 1: date published, 2: document type, 3: measure, 4: description, 5: view link
                        try:
                            file = tds[5].find(".//a").get('href')
                            title = tds[4].text
                            url = urljoin(result.url, file)
                            doc = {
                                'url': url,
                                'source_url': result.url,
                                'file_name': file,
                                'title': title,
                                'request_id': make_id(url)
                            }

                            context.emit(data=doc)
                        except IndexError(e):
                            context.emit_warning("Bad table structure [%s" % result.url)
            else:
                context.emit_warning("No documents table found [%s]" % result.url)