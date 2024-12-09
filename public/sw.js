importScripts(
    'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
);

const { registerRoute } =  workbox.routing;
const { precacheAndRoute } = workbox.precaching;

