/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'fspc.eu', // the auth0 domain prefix
    audience: 'cofee', // the audience set for the auth0 app
    clientId: 'xmLKgL2Zh8c6DUwPLSpz5wX1cCjOQZW9', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
