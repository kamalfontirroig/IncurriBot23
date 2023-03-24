function serviceWorkerIsUsed(){return 2<chrome.runtime.getManifest().manifest_version}if(serviceWorkerIsUsed())try{importScripts("browser_info.js","intern/utils.js")}catch(t){console.error("Failed to import scripts: ",t)}!function(){"use strict";async function a(t){await storageSet({com_tts_quickaccess_browser_extension_host:t})}async function r(){return(await storageGet("com_tts_quickaccess_browser_extension_host")).com_tts_quickaccess_browser_extension_host}async function o(){const t=chrome.runtime.connectNative("com.tts.quickaccess.browser.extension.host");t.onMessage.addListener(e)}async function n(){var t;t={applicationStateIsCloseConnection:!1,applicationStateIsCloseConnectionWithRestart:!0,operatingSystemSuspendOccurred:!1},await storageSet({com_tts_quickaccess_browser_extension_host:t}),await t,await o()}function e(t,e){var n=parseJSON(t);if(null!==n)switch(n.messageType){case"sendApplicationState":!async function(t){var e=await r();let n;n=e.applicationStateIsCloseConnection?{state:"terminate-native-host"}:{state:"running"};await t.postMessage(n)}(e);break;case"terminationHandshake":!async function(t){await async function(t){await t.postMessage({state:"received-terminate-native-host"}),t.disconnect()}(t);const e=await r();e.applicationStateIsCloseConnection=!1;t=e.applicationStateIsCloseConnectionWithRestart;e.applicationStateIsCloseConnectionWithRestart=!0,await a(e),t&&await o()}(e);break;case"sendBrowserInfo":!async function(t){await t.postMessage({browserInfo:getBrowserName()})}(e);break;case"sendActiveTabData":!function(t,e){e={getActiveTabDataConfig:{includeIFrames:e.includeIFrames,maxIFramesCount:e.maxIFramesCount},activeTabData:null};!function(a,r){chrome.tabs.query({active:!0,lastFocusedWindow:!0},function(t){try{const e=t[0];if(!e)return void c(a,r);if(!e.url)return void c(a,r);const n=e.id;if(!e.url.startsWith("http:")&&!e.url.startsWith("https:")&&!e.url.startsWith("file:"))return r.activeTabData={title:e.title,url:e.url,html:""},void c(a,r);injectJavaScriptInTab({tabId:n,injectInFrames:!1},{injectFunction:u,injectFunctionAsString:l},function(t){return!chrome.runtime.lastError&&t&&t.length?void(0!=t.length?(t=t[0].result,null!==(t=parseJSONString(t))?(r.activeTabData={title:e.title,url:e.url,html:t.html},r.getActiveTabDataConfig.includeIFrames?function(e,a,t,r){try{a.activeTabData.iframes=[],injectJavaScriptInTab({tabId:t,injectInFrames:!0},{injectFunction:m,injectFunctionAsString:d},function(t){if(chrome.runtime.lastError||!t||!t.length)return chrome.runtime.lastError&&chrome.runtime.lastError.message?console.error("Could not get iframe data of active tab:",chrome.runtime.lastError.message):console.error("Could not get iframe data of active tab."),void c(e,a);let n=0;t.forEach(function(t,e){t=t.result;!(a.getActiveTabDataConfig.maxIFramesCount<=0||n<a.getActiveTabDataConfig.maxIFramesCount)||null!==(t=parseJSONString(t))&&t.url!==r&&""!==t.url&&(n++,a.activeTabData.iframes.push({url:t.url,html:t.html}))}),c(e,a)})}catch(t){console.error("An error occurred in addIFrameDataToTabData: ",t),c(e,a)}}(a,r,n,e.url):c(a,r)):c(a,r)):c(a,r)):(chrome.runtime.lastError&&chrome.runtime.lastError.message?console.error("Could not get data of active tab:",chrome.runtime.lastError.message):console.error("Could not get data of active tab."),void c(a,r))})}catch(t){"Error: Tabs cannot be edited right now (user may be dragging a tab)."!==t&&console.error("An error occurred in getActiveTabData: ",t),c(a,r)}})}(t,e)}(e,n);break;case"event":!async function(t,e){switch(e.eventType){case"running-time-in-millis":await async function(t){24e4<=t&&await i(!0)}(parseInt(e.eventValue));break;case"on-operating-system-suspend":await async function(){const t=await r();t.operatingSystemSuspendOccurred=!0,await a(t),await i(!1)}();break;default:console.error("Received event of unknown type ",e.messageType)}await t.postMessage({eventState:"processed"})}(e,n);break;default:console.error("Received message of unknown type ",n.messageType),s(e)}else s(e)}async function i(t){const e=await r();e.applicationStateIsCloseConnection=!0,e.applicationStateIsCloseConnectionWithRestart=t,await a(e)}async function s(t){await t.postMessage({state:"error"})}async function c(t,e){e.activeTabData?await t.postMessage({...e.activeTabData}):await t.postMessage({state:"retry_sendActiveTabData",timeout:1e4})}function u(){try{return JSON.stringify({html:document.documentElement.innerHTML})}catch(t){return console.error("An error occurred in activeTabJavaScriptToInjectFunction: ",t),""}}serviceWorkerIsUsed()?(chrome.runtime.onInstalled.addListener(function(t){"install"!==t.reason&&"update"!==t.reason||n()}),chrome.management.onEnabled.addListener(function(t){chrome.runtime.id===t.id&&n()}),chrome.idle.onStateChanged.addListener(async function(t){if("active"==t){const e=await r();e.operatingSystemSuspendOccurred&&(e.operatingSystemSuspendOccurred=!1,await a(e),n())}})):n();const l='(function () {\n\ttry {\n\t\treturn JSON.stringify({\n\t\t\thtml: document.documentElement.innerHTML\n\t\t});\n\t}\n\tcatch (error) {\n\t\tconsole.error("An error occurred in activeTabJavaScriptToInjectFunctionAsString: ", error);\n\t\treturn "";\n\t}\n})();';function m(){try{return JSON.stringify({url:location.href,html:document.documentElement.innerHTML})}catch(t){return console.error("An error occurred in iframeOfActiveTabJavaScriptToInjectFunction: ",t),""}}const d='(function () {\n\ttry {\n\t\treturn JSON.stringify({\n\t\t\turl: location.href,\n\t\t\thtml: document.documentElement.innerHTML\n\t\t});\n\t}\n\tcatch (error) {\n\t\tconsole.error("An error occurred in iframeOfActiveTabJavaScriptToInjectFunctionAsString: ", error);\n\t\treturn "";\n\t}\n})();'}();