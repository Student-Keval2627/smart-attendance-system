const CACHE_NAME = "smartattend-static-v3";

const PRE_CACHE = [
    "/static/offline.html",
    "/static/icons/icon-192.png",
    "/static/icons/icon-512.png"
];


// ==========================================
// INSTALL
// ==========================================

self.addEventListener(
    "install",
    (event) => {

        event.waitUntil(
            caches
                .open(CACHE_NAME)
                .then((cache) => {
                    return cache.addAll(
                        PRE_CACHE
                    );
                })
        );

        self.skipWaiting();
    }
);


// ==========================================
// ACTIVATE
// ==========================================

self.addEventListener(
    "activate",
    (event) => {

        event.waitUntil(

            caches
                .keys()
                .then((keys) => {

                    return Promise.all(

                        keys
                            .filter(
                                (key) =>
                                    key !== CACHE_NAME
                            )
                            .map(
                                (key) =>
                                    caches.delete(key)
                            )

                    );

                })

        );

        self.clients.claim();
    }
);


// ==========================================
// FETCH
// ==========================================

self.addEventListener(
    "fetch",
    (event) => {

        const request = event.request;

        if (request.method !== "GET") {
            return;
        }


        const url = new URL(
            request.url
        );


        // ----------------------------------
        // STATIC FILES
        // ----------------------------------

        if (
            url.origin === self.location.origin
            &&
            url.pathname.startsWith(
                "/static/"
            )
        ) {

            event.respondWith(

                caches
                    .match(request)
                    .then((cached) => {

                        if (cached) {
                            return cached;
                        }

                        return fetch(request)
                            .then((response) => {

                                if (
                                    !response
                                    ||
                                    response.status !== 200
                                ) {
                                    return response;
                                }

                                const copy =
                                    response.clone();

                                caches
                                    .open(CACHE_NAME)
                                    .then((cache) => {

                                        cache.put(
                                            request,
                                            copy
                                        );

                                    });

                                return response;
                            });

                    })

            );

            return;
        }


        // ----------------------------------
        // HTML / FLASK PAGES
        // NETWORK ONLY
        // ----------------------------------

        if (request.mode === "navigate") {

            event.respondWith(

                fetch(request)
                    .catch(() => {

                        return caches.match(
                            "/static/offline.html"
                        );

                    })

            );

        }

    }
);