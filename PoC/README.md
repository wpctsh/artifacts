# Poc

Each folder in this directory contains the PoC for one specific provider.

In order to test those, different actions should be followed depending on each provider.

Cleverpush:
 - Visit `https://cleverpush.com/en/` and register a test account
 - Select `Dashboard`, `Create your first Platform`
 - Select `Setup now` besides `Web Push`
 - Step 1: Input your domain
 - Step 2: Choose a subdomain of `mycleverpush.com`, store the saved name
 - Continue and choose `Default Setup`
 - Follow the instructions to integrate it into your own website
 - Open `cleverpush/cleverpush.html`
   - Substitute `YOURSUBDOMAIN` with the chosen subdomain at step 2
   - Substitute `YOURDOMAIN` with your domain
 - Visit `cleverpush/cleverpush.html` in the browser at any address, it should show that you havn't yet visited the target website
 - Now visit and accept notifications on your domain
 - Visit `cleverpush/cleverpush.html` in the browser at any address, it should now show you the data of your subscription on your domain


LetReach:
 - Visit `https://www.letreach.com/` and register a test account
 - When registering, input your domain and choose a subdomain of `letreach.com`. Save the choosen name
 - Follow the instructions to integrate it into your own website
 - Open `letReach/letReach.html`
   - Substitute `YOURSUBDOMAIN` with the chosen subdomain
 - Visit `letReach/letReach.html` in the browser at any address, it should show that you havn't yet visited the target website
- Now visit and accept notifications on your domain
 - Visit `letReach/letReach.html` in the browser at any address, it should now that you have visited the target website



PushAlert:
 - Visit `https://pushalert.co/` and register a test account
 - When registering, make sure to select `http://` in the website section
 - In the `Branded Sub-domain` section choose a subdomain of `pushalert.co`. Save the choosen name
 - Follow the instructions to integrate it into your own website
 - Open `pushalert/pushAlert.html`
   - Substitute `YOURSUBDOMAIN` with the chosen subdomain
 - Visit `pushalert/pushAlert.html` in the browser at any address, it should show that you havn't yet visited the target website
 - Now visit and accept notifications on your domain
 - Visit `pushalert/pushAlert.html` in the browser at any address, it should now that you have visited the target website


VWO:
 - Select `Engage` on the menu
 - Follow the instructions to add new website
 - Make sure to add the website with `http://` and not `https://` as the protocol
 - Choose a custom subdomain of `pushcrew.com` when asked. Save the choosen name
 - Follow the instructions to integrate it into your own website
 - Open `vwo/vwo.html`
   - Substitute `YOURSUBDOMAIN` with the chosen subdomain
 - Visit `vwo/vwo.html` in the browser at any address, it should show that you havn't yet visited the target website
 - Now visit and accept notifications on your domain
 - Visit `vwo/vwo.html` in the browser at any address, it should now that you have visited the target website

Webpushr:
 - Visit `https://www.webpushr.com/` and register a test account
 - When registering your website, make sure to use `http://` and not `https://` as the protocol
 - Toggle the `My site is not fully HTTPS` box
 - Choose a subdomain of `wpush.io`. Save the choosen name
 - Follow the instructions to integrate it in your website
 - Open `webpushr/webpushr.html`
   - Substitute `YOURSUBDOMAIN` with the chosen subdomain
   - You may not need to update the public key too. In case it is required, you can find it in the code you included in your website during integration under the name `key`
 - Visit `webpushr/webpushr.html` in the browser at any address, it should show that you havn't yet visited the target website
 - Now visit and accept notifications on your domain
 - Visit `webpushr/webpushr.html` in the browser at any address, it should now that you have visited the target website

