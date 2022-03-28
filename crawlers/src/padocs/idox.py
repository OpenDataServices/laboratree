

def docs_url(context, data):
    # sets to 'Documents' tab
    url = data['url'].replace('activeTab=summary', 'activeTab=documents')
    context.emit(data={'url': url})


def parse(context, data):
    with context.http.rehash(data) as result:
        if result.html is not None:
            docstable = result.html.find(".//table[@id='Documents']")

            docs = []

            # for row in docstable.findall(".//tr"):
            #     # 0: checkbox, 1: document type, 2: measure, 3: description, 4: view link
            #     doc = {}