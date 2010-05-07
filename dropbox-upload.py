
import mechanize
import sys
import cookielib

def upload_file(user, password, file_path, dest_dir):
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    #            br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    br.open('http://dropbox.com')
    br.select_form(nr=1)
    br.form['login_email'] = user
    br.form['login_password'] = password
    br.submit()
    br.select_form(nr=13)
    br.form.set_all_readonly(False)
    br.form['dest'] = dest_dir
    f = open(file_path)
    br.form.add_file(f, None, file_path)
    br.submit()
    br.open('http://www.dropbox.com/logout');

if __name__ == '__main__':
    if len(sys.argv) > 4:
        upload_file(sys.argv[1] , sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print 'Wrong params'
        

