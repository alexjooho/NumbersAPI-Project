
from nums_api import app
from unittest import TestCase
from unittest.mock import patch, mock_open
from nums_api.fact_web_scrapers.names import names_web_scraper

SCRIPT_PATH = 'nums_api.fact_web_scrapers.names.names_web_scraper'
MOCK_HTML = '''
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
            <div class="browsename">
            <span class="listname">
                <a href="/name/aabraham" class="nll">Aabraham</a>
            </span>
            <span class="listgender">
                <span class="masc" title="masculine">m</span>
            </span>
            <span class="listusage">
                <a href="/names/usage/finnish" class="usg">Finnish (Rare)</a>
            </span>
            <br>
            Finnish form of 
            <a href="/name/abraham" class="nl">Abraham</a>.
            </div>
            </body>
</html>
            '''

TEST_INPUT = 'TEST INPUT'


class TestPageParser(TestCase):
    def test_page_parser(self):
        with patch(f'{SCRIPT_PATH}.requests.get') as mock_request:
            mock_request.return_value.content = MOCK_HTML
            
            self.assertEqual(names_web_scraper.parse_a_page('http://www.fake.com'), True)
            
            mock_request.return_value.content = TEST_INPUT
            self.assertEqual(names_web_scraper.parse_a_page('http://www.fake.com'), False)
        
       
class TestFileWriter(TestCase):
    def test_file_writer(self):
        fake_file_path = "fake/file/path"
        content = "Test message for file."
        with patch(f'{SCRIPT_PATH}.open', mock_open()) as mocked_file:
            names_web_scraper.write_to_file(fake_file_path, content)

            # assert if opened file on write mode 'w'
            mocked_file.assert_called_once_with(fake_file_path, 'w')

            # assert if write(content) was called from the file opened
            # in another words, assert if the specific content was written in file
            mocked_file().write.assert_called_once_with(content)