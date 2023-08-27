# Building the instrumented chromium version and running the crawler

## Building chromium

The following instructions are needed to correctly build the instrumented version of chromium
The build was executed on a VM with ubuntu:20.04

 - Clone the `depot_tools` from `https://chromium.googlesource.com/chromium/tools/depot_tools.git`
 - Add the `depot_tools` to the PATH environment variable
 - Disable the `depot_tools` automatic updated by setting the `DEPOT_TOOLS_UPDATE` environment variable to `0`
 - Clone the chromium source code by running `fetch --nohooks chromium`
 - Checkout the correct commit: `5aac797b386d9fd1e655ff30558ce10a2d295259`
 - Obtain the commit date: `COMMIT_DATE=$(git log -n 1 --pretty=format:%ci)`
 - Get the correct commit of the `depot_tools` by running `git rev-list -n 1 --before="$COMMIT_DATE" main`
 - Checkout the correct commit of the `depot_tools`
 - Run `git clean -ffd` in the `depot_tools` directory
 - Run `gclient sync -D --force --reset  --with_branch_heads` in the chromium directory
 - Run `./build/install-build-deps.sh` in the chromium directory
 - Run `gclient runhooks` in the chromium directory
 - Apply the first patch by running `git apply instrument-patch1.diff` in the chromium directory
 - Apply the second patch by running `git apply instrument-patch2.diff` in the chromium directory
 - Move `logger.cc` to `src/third_party/blink/renderer/modules/service_worker/logger.cc` in the chromium directory
 - Move `logger.h` to `src/third_party/blink/renderer/modules/service_worker/logger.h` in the chromium directory
 - Run `gn gen out/Instrumented` in the chromium directory
 - Run `autoninja -C out/Instrumented chrome` in the chromium directory
 - You can find the built chromium in the out/Instrumented directory

## Compile time

Compiling Chromium can vary in duration, taking anywhere from minutes to several hours, depending on the number of cores available on the machine.

## Running the crawler

Both `visit.js` and `third_party_detection.js` require the path to chromium to be set correctly inside the scripts. Specifically the `INSTRUMENTED_CHROMIUM_PATH` variable should point to a valid `chrome` executable.

Moreover, both scripts require `puppeteer` and `node-fetch@2` to be installed.

Both codes can now be run with `node <script.js> <target>`

