const puppeteer = require('puppeteer');
const fs = require('fs');
const dns = require('dns');
const fetch = require('node-fetch');
const { exit } = require('process');
var urlparser = require('url');

const WAIT_TIME_FOR_NOTIFICATION_REQUEST = 15000;
const INSTRUMENTED_CHROMIUM_PATH = "";

if (process.argv.length != 3) {
    console.log("Usage: visit.js <url>");
    process.exit(0);
}
let url = process.argv[2]
if (!url.endsWith("/")) {
    url = url + "/"
}
const base_results_path = process.cwd() + "/results/" + urlparser.parse(url).hostname + "/";

(async () => {

    fs.rmSync(base_results_path + ".config", { recursive: true, force: true });
    fs.rmSync(base_results_path + ".pki", { recursive: true, force: true });
    process.env["HOME"] = base_results_path;

    const ips=await new Promise((resolve, reject) => {
        dns.resolve4(url.replace("https://", "").replace("http://", "").replace("/", ""), (err, addresses)=>{
            resolve(addresses);
    })});

    if(ips===undefined || ips.length<=0){
        let result = { url, "exception": "no DNS response"}
        console.log(JSON.stringify(result));
        process.exit(0);
    }

    const browser = await puppeteer.launch({ env: process.env, args: ['--no-sandbox', '--ignore-certificate-errors'], executablePath: INSTRUMENTED_CHROMIUM_PATH, headless: true })

    let page = await browser.newPage()
    await page.setDefaultNavigationTimeout(60000);

    try {
        await page.goto(url, { waitUntil: "networkidle0" });
    } catch {

    }

    await new Promise(r => setTimeout(r, WAIT_TIME_FOR_NOTIFICATION_REQUEST));

    let pageHTML = await Promise.race([ //Some websites never returns from this, and page.evaluate doesn't implement a timeout by itself. This prevents hanging on such rare websites
        page.evaluate(() => document.querySelector('*').outerHTML),
        new Promise(r => setTimeout(r, 15000))
    ]);

    if (pageHTML == undefined) {
        pageHTML = ""
    }

    if (pageHTML.includes("j.src = 'https://www.googletagmanager.com/gtm.js?id=")) {
        let tmp = pageHTML.split("j.src = 'https://www.googletagmanager.com/gtm.js?id=");
        if (tmp.length == 2) {
            tmp = tmp[1].split("GTM-");
            if (tmp.length >= 2) {
                let id = "GTM-" + tmp[1].split(")")[0].replace("'", "").replace('"', '')
                const gtm_data = await fetch("https://www.googletagmanager.com/gtm.js?id=" + id)
                if (gtm_data.ok) {
                    const html = await gtm_data.text()
                    pageHTML = pageHTML + html;
                }
            }
        }
    }

    let pushengage = false;
    let pushnami = false;
    let pushpad = false;
    try {
        const sw_data = await fetch(url + "service-worker.js")
        if (sw_data.ok) {
            const html = await sw_data.text()
            if (html.includes("pushengage.com")) {
                pushengage = true;
            }
            if (html.includes("api.pushnami.com")) {
                pushnami = true;
            }
            if (html.includes("pushpad.xyz")) {
                pushpad = true;
            }
        }
    } catch {

    }

    let izooto = false
    try {
        const izooto_data = await fetch(url + "izooto.html")
        if (izooto_data.ok) {
            const html = await izooto_data.text()
            if (html.includes("cdn.izooto.com")) {
                izooto = true;
            }
        }
    } catch {

    }
    let najva = false;
    try {
        
        const najva_data = await fetch(url + "najva-messaging-sw.js")
        if (najva_data.ok) {
            const html = await najva_data.text()
            if (html.includes("app.najva.com")) {
                najva = true;
            }
        }
    } catch {

    }

    let pushalert = pageHTML.includes("cdn.pushalert.co")
    if (pushalert == false) {
        try {
            const pushalert_data = await fetch(url + "sw.js")
            if (pushalert_data.ok) {
                const html = await pushalert_data.text()
                if (html.includes("cdn.pushalert.co")) {
                    pushalert = true;
                }
            }
        } catch {

        }
    }

    let notix = false;
    try {
        const notix_data = await fetch(url + "sw.enot.js")
        if (notix_data.ok) {
            const html = await notix_data.text()
            if (html.includes("notix.io")) {
                notix = true;
            }
        }
    } catch {

    }

    let batch = false;
    try {
        const batch_data = await fetch(url + "batchsdk-worker-loader.js")
        if (batch_data.ok) {
            const html = await batch_data.text()
            if (html.includes("batch.com")) {
                batch = true;
            }
        }
    } catch {

    }

    let frizbit = false;
    try {
        const frizbit_data = await fetch(url + "FrizbitServiceWorker.js")
        if (frizbit_data.ok) {
            const html = await frizbit_data.text()
            if (html.includes("frizbit")) {
                frizbit = true;
            }
        }
    } catch {

    }


    let pushpanda = false;
    try {
        const pushpanda_data = await fetch(url + "PushPandaWorker.js")
        if (pushpanda_data.ok) {
            const html = await pushpanda_data.text()
            if (html.includes("pushpanda")) {
                pushpanda = true;
            }
        }
    } catch {

    }

    let killtarget = false;
    try {
        const killtarget_data = await fetch(url + "kt-messaging.js")
        if (killtarget_data.ok) {
            const html = await killtarget_data.text()
            if (html.includes("killtarget")) {
                killtarget = true;
            }
        }
    } catch {

    }

    let letReach = pageHTML.includes("ltr-btn-allow")

    let oneSignal = pageHTML.includes("OneSignalSDK")

    let webpushr = pageHTML.includes("webpushr")

    let gravitec = pageHTML.includes("cdn.gravitec.net")

    let cleverpush = pageHTML.includes("cleverpush.com")

    let pushly = pageHTML.includes("pushly")

    let truepush = pageHTML.includes("truepush")

    let vwo = pageHTML.includes("pushcrew")

    let subscribers = pageHTML.includes("cdn.subscribers.com") 

    let wonderpush = pageHTML.includes("wonderpush.com")

    let pushpushgo = pageHTML.includes("pushpushgo.com")

    let foxpush = pageHTML.includes("foxpush")

    let jeeng = pageHTML.includes("jeeng.com")

    let pushwoosh = pageHTML.includes("Pushwoosh")

    let pushworld = pageHTML.includes("push.world")

    let push4site = pageHTML.includes("push4site")

    if (pushpad == false) {
        pushpad = pageHTML.includes("pushpad.xyz")
    }

    let pushe = pageHTML.includes("pushe.co")

    let pushpros = pageHTML.includes("pushpros.tech")

    let pushmonkey = pageHTML.includes("pushmonkey.com")

    let pushnews = pageHTML.includes("pushnews") || pageHTML.includes("pn.vg")

    let pushtoast = pageHTML.includes("pushtoast")

    let titanpush = pageHTML.includes("titanpush")

    let pushbird = pageHTML.includes("cdn.pushbird.com")

    let magicbell = pageHTML.includes("magicbell")

    let popify = pageHTML.includes("popify.app")

    let panneaupocket = pageHTML.includes("app.panneaupocket.com")

    let quickblox = pageHTML.includes("quickblox")

    await browser.close();

    aimtell = false;
    const path = base_results_path + "sw_scripts_output.log";
    if (fs.existsSync(path)) {
        const data = fs.readFileSync(path, "utf-8");
        if (data.includes("cdn.aimtell.com")) {
            aimtell = true;
        }
    }

    let result = { url, isHttps: url.startsWith("https"), thirdParties: { letReach, oneSignal, webpushr, izooto, gravitec, pushengage, cleverpush, pushly, truepush, vwo, pushnami, aimtell, najva, subscribers, wonderpush, pushalert, notix, pushpushgo, foxpush, batch, jeeng, pushwoosh, pushworld, push4site, pushpad, pushe, pushpros, pushmonkey, frizbit, pushpanda, killtarget, pushnews, pushtoast, titanpush, pushbird, magicbell, popify, panneaupocket, quickblox } }
    console.log(JSON.stringify(result));

    process.exit(0);

})()


process.on('uncaughtException', function (err) {
    if (err) {
        let result = { url, "exception": err.stack+" "+err.name+" "+err.message}
        console.log(JSON.stringify(result));
        process.exit(0);
    }
});


process.on('unhandledRejection', function (reason, p) {
        let result = { url, "exception": "unhandledRejection"}
        console.log(JSON.stringify(result));
        process.exit(0);
});
