import { useAuthStore } from '@/stores';

export const fetchWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE')
};

function request(method) {
    return (url, body) => {
        const requestOptions = {
            method,
            headers: authHeader(url),
            url,
            credentials: 'include' // withCredentials to true
        };
        if (body) {
            if (url.endsWith('access-token')) {
                requestOptions.headers['Content-Type'] = 'application/x-www-form-urlencoded';
                requestOptions.body = new URLSearchParams(body);
            } else {
                requestOptions.headers['Content-Type'] = 'application/json';
                requestOptions.body = JSON.stringify(body);
            }
        }
        return fetch(url, requestOptions).then(handleResponse);
    }
}

// helper functions

function authHeader(url) {
    // return auth header with jwt if user is logged in and request is to the api url
    const { user } = useAuthStore();
    const isLoggedIn = !!user?.access_token;
    const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL);
    if (isLoggedIn && isApiUrl) {
        return { Authorization: `Bearer ${user.access_token}` };
    } else {
        return {};
    }
}

async function handleResponse(response, requestOptions, retry = true) {
    const isJson = response.headers?.get('content-type')?.includes('application/json');
    const data = isJson ? await response.json() : null;

    // check for error response
    if (!response.ok) {
        const { logout, refreshAccessToken } = useAuthStore();
        if ([401].includes(response.status) && retry) {
            try {
                await refreshAccessToken();
                return fetch(requestOptions.url, requestOptions).then(response => handleResponse(response, requestOptions, false));
            } catch (error) {
                // auto logout if refreshing access token fails
                logout();
            }
        }

        // get error message from body or default to response status
        const error = (data && data.message) || response.status;
        return Promise.reject(error);
    }

    return data;
}
