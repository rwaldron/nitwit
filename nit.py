import urllib
import optparse
import os.path
import pickle


def truncate(message,limit):
    if len(message) > limit:
        # break off at 137 chars and concat elipsis
        return message[:(limit-3)] + '...'
    else:
        # not too long
        return message

def post(opts, credentials):
    # only post to twitter if the message wasn't blank
    if opts.message != '':
        urllib.urlopen(
            "http://%s:%s@twitter.com/statuses/update.xml" % (credentials['username'],credentials['password']), 
            urllib.urlencode({
                "status" : truncate(opts.message,140)
            })
        )
        print("\n\n'"+opts.message+"' \n\n>>> posted successfully\n\n")
    else:
        print("No Message? No Post. Those are the rules.\n\n")
    
    return

# main command line program
def main():
    # set up the option parser
    parser = optparse.OptionParser()
    # define this program's accepted option set
    parser.add_option(
        '--message', '-m', 
        default='' , help="Be sure to put your message in quotes :)"
    )
    parser.add_option(
        '--username', '-u', 
        default='' , help="Twitter username"
    )
    parser.add_option(
        '--password', '-p', 
        default='' , help="Twitter password"
    )        
    # parse the opts passed
    opts, arguments = parser.parse_args()
    
    if os.path.exists(".account"):
        # conf exists, use pickle to load the stored object
        credentials = pickle.load(open(".account", "r"))
        
    else:
        # conf file does not exist:
        # check first to see if credentials have been passed in as options 
        # otherwise prompt for credentials
        # allows mix and match input       
        credentials = { 
            "username": opts.username if opts.username != '' 
                                      else raw_input("Twitter username: "), 
            "password": opts.password if opts.password != '' 
                                      else raw_input("Twitter password: ") 
        }

        pickle.dump(credentials, open(".account", "w"))
    
    post(opts, credentials)
    return

#compile: python nit_compile.py
#
#usage:   python nit -m "posting to twitter"
#usage:   python nit -m "posting to twitter" -u username -p password
    
if __name__ == '__main__':
    main()        
