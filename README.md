# Artifacts for paper #191 

Artifact release for ACSAC 2023 submission entitled "When Push Comes to Shove: Empirical Analysis of Web Push Implementations in the Wild".


Directories and files included:
 - `analyzer/*`: This folder contains the python script used to analyze the results obtained by the crawler alongside the results themselves.
   - `analyzer/top500k.csv`: The exact version of the Tranco top 500K list we used for our large-scale measurement described in section 5.1 of the paper.
   - `analyzer/sw-results.log`: The output of `crawler/visit.js` for all websites for which it did complete correctly.
   - `analyzer/3p-measurement.part*.log`: The output of `crawler/third_party_detection.js` for all websites for which it did complete correctly.
   - `analyzer/analyze_all.py`: A python script to analyze the above files and output the results presented in the paper.

 - `crawler/*`: This folder contains the javascript scripts used to crawl each website and output the results.
   - `crawler/package.json` and `crawler/package-lock.json`: Files to install the required dependencies. 
   - `crawler/visit.js`: JavaScript file which runs the dynamic and static approaches. It takes the target URL as the single parameter.
   - `crawler/third_party_detection.js`: JavaScript file which runs the third-party detection. It takes the target URL as the single parameter.
   - `crawler/chromium-patch/*`: Directory containing all patches we made to chromium in order to instrument it.
     - `crawler/chromium-patch/instrument-patch1.diff`: First patch, logging all calls to several web-push related APIs, as described in section 5.1 of the paper.
     - `crawler/chromium-patch/instrument-patch2.diff`: Second patch, enabling automatic acceptance of web push notification requests by the browser, as described in section 5.1 of the paper.
     - `crawler/chromium-patch/logger.cc` and `crawler/chromium-patch/logger.h`: file-logger used by the above patches.
   - `crawler/README.md`: Instructions for building the instrumented version of chromium and using the `crawler/visit.js` and `crawler/third_party_detection.js` scripts.

 - `PoC/*`: This folder contains the PoC for the vulnerable third-party providers. Note that some of those vulnerabilities may have already been patched and the PoC may not be working anymore.
   - `PoC/README.md`: The readme on how to test the proof of concepts.