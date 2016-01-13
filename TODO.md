
# TODO
## OAuth2
> If you’re application requires access to other Coinbase users' accounts, do not use API Key. To securely access other Coinbase users' accounts, use Coinbase Connect (OAuth2)
	
* Python Social Auth http://psa.matiasaguirre.net/
* with Coinbase Strategy http://psa.matiasaguirre.net/docs/backends/coinbase.html
* after registering New OAuth2 Application at https://sandbox.coinbase.com/oauth/applications/new

## Security
* store the API_SECRET in a good way
* validate SSL certificate
* whitelist the app IP !
https://developers.coinbase.com/docs/wallet/api-key-authentication#security-best-practices

### 12factor app
where to store the API_SECRET ? 

> A litmus test for whether an app has all config correctly factored out of the code is whether the codebase could be made open source at any moment, without compromising any credentials.

http://12factor.net (also read the whole thing)

Right now I am keeping the API_SECRET in a file which is mentioned in .gitignore  = not bad, but not perfect.

 
 