# encoding: utf-8

import pycurl
import sys

try:
    # Python 3
    from io import BytesIO
except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO


class Curl:
    __user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110'

    def __request(self, url, type, data, timeout, header):

        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT, self.__user_agent)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.TIMEOUT, timeout)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.SSL_VERIFYHOST, False)

        buffer_body = BytesIO()
        buffer_header = BytesIO()
        c.setopt(pycurl.WRITEFUNCTION, buffer_body.write)
        c.setopt(pycurl.HEADERFUNCTION, buffer_header.write)

        result = {'status': 200, 'body': '', 'header': [], 'error': ''}
        try:
            c.perform()
        except:
            error = sys.exc_info()[1]
            result['status'] = error[0]
            result['error'] = error[1]

        result['body'] = buffer_body.getvalue().decode('utf-8')
        result['header'] = self.__parse_header(buffer_header.getvalue().decode('utf-8'))
        buffer_body.close()
        buffer_header.close()
        return result

    def __parse_header(self, header):
        header_list = {}
        for one in header.split('\r\n'):
            if ': ' in one:
                header_key_value = one.split(': ')
                if len(header_key_value) == 2:
                    key, value = header_key_value
                    header_list[key] = value
        return header_list

    def get(self, url, timeout=10, header=None):
        return self.__request(url, 'get', [], timeout, header)

    def post(self, url, data=None, timeout=10, header=None):
        return self.__request(url, 'post', data, timeout, header)

    def download(self):
        return
