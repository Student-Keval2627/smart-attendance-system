let deferredInstallPrompt = null;


// ==========================================
// SERVICE WORKER
// ==========================================

if ("serviceWorker" in navigator) {

    window.addEventListener(
        "load",
        () => {

            navigator.serviceWorker
                .register(
                    "/service-worker.js"
                )
                .then(() => {

                    console.log(
                        "SmartAttend service worker registered."
                    );

                })
                .catch((error) => {

                    console.error(
                        "Service worker registration failed:",
                        error
                    );

                });

        }
    );

}


// ==========================================
// INSTALL BUTTON
// ==========================================

const installButton =
    document.createElement("button");

installButton.id =
    "pwa-install-btn";

installButton.type =
    "button";

installButton.textContent =
    "Install SmartAttend";

installButton.hidden = true;


document.addEventListener(
    "DOMContentLoaded",
    () => {

        document.body.appendChild(
            installButton
        );

    }
);


// ==========================================
// INSTALL PROMPT
// ==========================================

window.addEventListener(
    "beforeinstallprompt",
    (event) => {

        event.preventDefault();

        deferredInstallPrompt =
            event;

        installButton.hidden =
            false;

    }
);


// ==========================================
// INSTALL CLICK
// ==========================================

installButton.addEventListener(
    "click",
    async () => {

        if (!deferredInstallPrompt) {
            return;
        }

        deferredInstallPrompt.prompt();

        await deferredInstallPrompt.userChoice;

        deferredInstallPrompt =
            null;

        installButton.hidden =
            true;

    }
);


// ==========================================
// INSTALLED
// ==========================================

window.addEventListener(
    "appinstalled",
    () => {

        deferredInstallPrompt =
            null;

        installButton.hidden =
            true;

    }
);