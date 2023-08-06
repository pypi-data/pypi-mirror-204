from cnki_html2json import html2json

def test_html2json():
    with open('test/fulltext.html','r') as f:
        content = f.read()

    text_structure = html2json.ExtractContent(content,'structure').extract_all()
    assert text_structure['body_text']['1 引言']['text'][:3] == "近年来"

    text_plain = html2json.ExtractContent(content,'plain').extract_all()
    assert text_plain['body_text'][:3] == "近年来"

    text_raw = html2json.ExtractContent(content,'raw').extract_all()
    assert '[1]' in text_raw['body_text']['1 引言']['text']