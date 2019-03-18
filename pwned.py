# function to check the arguments passed to our script from the command line
def get_pass():
    # Get password from command line
    executable = sys.argv[0]
    try:
        password = sys.argv[1]
    except IndexError:
        print("No password supplied")
        exit(1)

    return password


def hashPassword():
    # Get pass from command line, hash it with SHA1, and return the hash
    password = get_pass()
    SHA1 = hashlib.sha1(password.encode('utf-8'))
    hashed_pass = SHA1.hexdigest()

    return hashed_pass


# Import necessary modules
import requests
import hashlib
import sys

base_url = 'https://api.pwnedpasswords.com/range/'
user_agent = {
    'User-Agent': 'Personal-Crypto-Project',
    'From': 'nleroy917@gmail.com'
}

# Hash password and get first 5 characters
pass_hash = hashPassword().upper()
prefix = pass_hash[0:5]

# Send request to API and parse response
response = requests.get(base_url + pass_hash[:5], headers=user_agent)
found_hashes = response.text.split('\r\n')

flag = 0

# iterate through repsonse and search for a match
for hash in found_hashes:

    # create potential hash
    potential_hash = prefix + hash[0:hash.find(':')]

    # check for match
    if potential_hash == pass_hash:
        print('Password Leaked')
        print(prefix + hash)
        flag = 1
        break

if not flag:
    print('No Leak Detected')

exit(0)
