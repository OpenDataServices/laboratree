import logging
import hashlib


from memorious.helpers.key import make_id


log = logging.getLogger(__name__)


def docs_url(context, data):
    url = '%s&tab=2' % data['url'] # sets to 'Associated Documents' tab
    context.emit(data={'url': url})


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
                hidden_inputs['__EVENTARGUMENT'] = doc['postbackarg']
                response = context.http.post(data.get('url'), data=hidden_inputs)

                document_data = {
                    'content_hash': response.content_hash,
                    'request_id': make_id(data.get('url'), doc.get('file_name', response.content_hash)),
                    'url': data.get('url'),
                    'title': doc.get('title', ''),
                    'file_name': doc.get('file_name','')
                }
                context.emit(data=document_data)


def get_document_args(form):
    """
    Parse args from js onclick events for one post request per document.
    ie. __doPostBack('ctl00$MainContent$gridDocuments','rc0')
    """
    docs = []
    table = form.find(".//table[@id='MainContent_gridDocuments']")
    for tr in table.findall(".//tr"):
        doc = {}
        onclick = tr.get('onclick')
        if onclick is not None:
            doc['postbackarg'] = onclick.split(',')[1].strip(')').strip("'")
            doc['title'] = tr.find(".//a").text
            hids = [hid.value for hid in tr.findall(".//input[@type='hidden']") if 'hidFullFileName' in hid.name]
            if len(hids) > 0:
                doc['file_name'] = hids[0] # Assuming there's only one of these
            docs.append(doc)

    return docs
