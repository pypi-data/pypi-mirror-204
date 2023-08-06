from authenticate import authenticate

def test_authenticate():
    sdk = authenticate()
    access_token, token_type = sdk.authenticate('burak', 'burak')
    print(access_token)
    print(token_type)

test_authenticate()
