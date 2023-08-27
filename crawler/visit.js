const puppeteer = require('puppeteer');
const fs = require('fs');
const fetch = require('node-fetch');
const { exit } = require('process');
var urlparser = require('url');

const WAIT_TIME_FOR_NOTIFICATION_REQUEST = 60000;
const INSTRUMENTED_CHROMIUM_PATH = "";

if (process.argv.length != 3) {
    console.log("Usage: visit.js <url>");
    exit(0)
}
const url = process.argv[2]

if (!url.endsWith("/")) {
    url = url + "/"
}

const base_results_path = process.cwd() + "/results/" + urlparser.parse(url).hostname + "/";

(async () => {

    fs.rmSync(base_results_path + ".config", { recursive: true, force: true });
    fs.rmSync(base_results_path + ".pki", { recursive: true, force: true });
    process.env["HOME"] = base_results_path;
    const browser = await puppeteer.launch({ env: process.env, args: ['--no-sandbox'], executablePath: INSTRUMENTED_CHROMIUM_PATH, headless: true })
    
    let page = await browser.newPage()
    await page.setDefaultNavigationTimeout(60000);
    try{
        await page.goto(url, { waitUntil: "networkidle0" });
    }catch{

    }
    await new Promise(r => setTimeout(r, WAIT_TIME_FOR_NOTIFICATION_REQUEST));

    await browser.close();
    let sw = false;
    let dynamic = false;
    let static = false;
    let path = base_results_path + "sw_apicalls_output.log";
    if (fs.existsSync(path)) {
        const data = fs.readFileSync(path, "utf-8");
        if (data.length > 0) {
            sw = true; //A sw has been installed
        }
        if (data.includes("Notification::requestPermission") || data.includes("PushManager.subscribe")) {
            dynamic = true; //A notification request has been made
        }
    }
    if (sw == true && dynamic==false) { //If a sw has been installed and no request was made, use the static approach
        path = base_results_path + "sw_scripts_output.log";
        if (fs.existsSync(path)) {
            const data = fs.readFileSync(path, "utf-8");
            const lines = data.split("\n");
            let sw_script = "";
            for (const line of lines) {
                const url = line.split(" ")[0].replace("main---", "").replace(/"/g, "")
                if (url.startsWith("http")) {
                    const response = await fetch(url, { "headers": { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" } });
                    if (response.ok) {
                        sw_script += await response.text();
                    }
                }
            }
            if (sw_script.includes("addEventListener('push'") || sw_script.includes('addEventListener("push"') || sw_script.includes('push notification') || sw_script.includes('vapidPublicKey') || sw_script.includes("notificationclick") || sw_script.includes("handlePushEvent")) {
                static = true;
            }
        }
    }else if(dynamic==true){
        static=true;
    }
    let result={url,sw, dynamic, static}
    console.log(JSON.stringify(result));



}) ()
