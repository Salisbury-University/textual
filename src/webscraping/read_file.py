import urllib.request

if __name__=="__main__":
    url_str = " "
  
    print("Checking " + url_str + " | Returned: ", end='')
    try:
            status_code = urllib.request.urlopen(url_str).getcode()
    except urllib.error.HTTPError as err:
        print('HTTP', err.code, 'ERROR')

    if status_code != 400:
        print(status_code, end='\n')
