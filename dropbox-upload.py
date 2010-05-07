import mechanize
from getpass import getpass
import sys
from os import environ
import cookielib
from urllib2 import HTTPError

class UploadError(Exception): pass

def upload_file(user, password, file_path, dest_dir):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    br.open('http://dropbox.com')
    br.select_form(nr=1)
    br.form['login_email'] = user
    br.form['login_password'] = password
    rs = br.submit()
    if rs.read().find('Log out') == -1:
        raise UploadError('Authorization failed')

    br.select_form(nr=13)
    br.form.set_all_readonly(False)
    br.form['dest'] = dest_dir
    f = open(file_path)
    br.form.add_file(f, None, file_path)
    try:
        br.submit()
    except HTTPError, e:
        if e.code == 404:
            pass
    br.open('http://www.dropbox.com/logout');


if __name__ == '__main__':
    try:
        password = environ.get('DROPBOX_PASSWORD')
        if len(sys.argv) != 4:
            raise UploadError('Wrong params quantity')

        if password is None:
            password=getpass('Enter password: ')
        if len(password) == 0:
            raise UploadError('You have to enter password or set up DROPBOX_PASSWORD environment variable')

        upload_file(sys.argv[1] , password, sys.argv[2], sys.argv[3])

    except UploadError, e:
        print 'Upload error: %s' % e

