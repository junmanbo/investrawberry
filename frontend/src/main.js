import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import { router } from './router';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.mount('#app');



import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import { router } from './helpers';
import { useAuthStore } from './stores';

startApp();

// async start function to enable waiting for refresh token call
async function startApp () {
    const app = createApp(App);

    app.use(createPinia());
    app.use(router);

    // attempt to auto refresh token before startup
    try {
        const authStore = useAuthStore();
        await authStore.refreshAccessToken();
    } catch (error) {
        // catch error to start app on success or failure
        console.log(error);
    }

    app.mount('#app');
}
