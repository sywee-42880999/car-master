const CACHE='car-master-v1';
const ASSETS=['./','./index.html','./app.js','./style.css','./manifest.webmanifest','./data/parts.json','./data/vehicles.json','./images/placeholder-suv.svg'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS))));
self.addEventListener('fetch',e=>e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request))));
