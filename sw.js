const CACHE = 'car-master-black-v07';
const ASSETS = [
  './',
  './index.html',
  './black-preview.html',
  './black-preview.css?v=1',
  './black-preview.js?v=1',
  './app.js?v=5',
  './style.css?v=5',
  './style-v04.css?v=5',
  './manifest.webmanifest',
  './data/parts.json',
  './data/master.json',
  './data/source_registry.json',
  './data/vehicles.json',
  './images/venue/front.jpg',
  './images/venue/rear.jpg',
  './images/venue/side.jpg',
  './images/placeholder-suv.svg'
  ,'./images/parts/0011.jpg'
  ,'./images/parts/0012.jpg'
  ,'./images/parts/0013.jpg'
  ,'./images/parts/0014.jpg'
  ,'./images/parts/0015.jpg'
  ,'./images/parts/0016.jpg'
  ,'./images/parts/0017.jpg'
  ,'./images/parts/0018.jpg'
  ,'./images/parts/0019.jpg'
  ,'./images/parts/0020.jpg'
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