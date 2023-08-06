from cnki_html2json import html2json

def test_fulltext():
    with open('tests/fulltext.html','r') as f:
        content = f.read()

    text_structure = html2json._ExtractContent(content,'structure').extract_all()
    assert text_structure['body_text']['1 引言']['text'][:14] == '近年来，以Chat GPT('
    assert text_structure['body_text']['1 引言']['reference'][0]==1

    text_plain = html2json._ExtractContent(content,'plain').extract_all()
    assert text_plain['body_text'][:14] == '近年来，以Chat GPT('

    text_raw = html2json._ExtractContent(content,'raw').extract_all()
    assert '[1]' in text_raw['body_text']['1 引言']['text']

def test_fulltext_crawl():
    with open('tests/fulltext_crawl.html','r') as f:
        content = f.read()

    text_structure = html2json._ExtractContent(content,'structure').extract_all()
    assert text_structure['body_text']['1 引言']['text'][:14] == '近年来，以Chat GPT('
    assert text_structure['body_text']['1 引言']['reference'][0]==1

    text_plain = html2json._ExtractContent(content,'plain').extract_all()
    assert text_plain['body_text'][:14] == '近年来，以Chat GPT('

    text_raw = html2json._ExtractContent(content,'raw').extract_all()
    assert '[1]' in text_raw['body_text']['1 引言']['text']