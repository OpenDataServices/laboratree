import logging
import memorious.operations.parse
import hashlib


log = logging.getLogger(__name__)


def parse(context, data):
    with context.http.rehash(data) as result:
        if result.html is not None:
            form = result.html.find(".//form[@id='form1']")
            hidden = form.findall(".//input[@type='hidden']")

            hidden_inputs = {
                h_in.get('name'): h_in.get('value')
                for h_in in hidden
            }
            hidden_inputs['__EVENTTARGET'] = 'ctl00$MainContent$gridDocuments'
            docs = get_document_args(form)
            for doc in docs:
                hidden_inputs['__EVENTARGUMENT'] = doc
                response = context.http.post(data.get('url'), data=hidden_inputs)
                context.emit(data={'content_hash': response.content_hash})


def get_document_args(form):
    """
    Parse args from js onclick events for one post request per document.
    ie. __doPostBack('ctl00$MainContent$gridDocuments','rc0')
    """
    docs = []
    table = form.find(".//table[@id='MainContent_gridDocuments']")
    for tr in table.findall(".//tr"):
        doc = tr.get('onclick')
        if doc is not None:
            doc = doc.split(',')[1].strip(')').strip("'")
            docs.append(doc)
    return docs
