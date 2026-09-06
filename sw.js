const CACHE = 'car-master-v05';
const ASSETS = [
  './',
  './index.html',
  './app.js?v=5',
  './style.css?v=5',
  './style-v04.css?v=5',
  './manifest.webmanifest',
  './data/parts.json',
  './data/vehicles.json',
  './images/venue/front.jpg',
  './images/venue/rear.jpg',
  './images/venue/side.jpg',
  './images/placeholder-suv.svg'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE).then(cache => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html')))
  );
});
