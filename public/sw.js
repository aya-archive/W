// A.U.R.A Service Worker
// Provides offline functionality and caching for the PWA

const CACHE_NAME = 'aura-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/',
  '/static/js/',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Install event - cache resources
self.addEventListener('install', (event) => {
  console.log('A.U.R.A Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('A.U.R.A Service Worker caching files');
        return cache.addAll(urlsToCache);
      })
      .catch((error) => {
        console.log('A.U.R.A Service Worker cache failed:', error);
      })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
      .catch(() => {
        // Return offline page if available
        return caches.match('/offline.html');
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('A.U.R.A Service Worker activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('A.U.R.A Service Worker deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Handle background sync for offline data
self.addEventListener('sync', (event) => {
  if (event.tag === 'aura-data-sync') {
    console.log('A.U.R.A Service Worker syncing data...');
    event.waitUntil(syncData());
  }
});

// Sync function for offline data
async function syncData() {
  try {
    // Implement data synchronization logic here
    console.log('A.U.R.A Service Worker data sync completed');
  } catch (error) {
    console.log('A.U.R.A Service Worker sync failed:', error);
  }
}
