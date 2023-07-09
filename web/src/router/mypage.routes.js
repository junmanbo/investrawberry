import { Layout, Mypage, ApiKey } from '@/views/mypage';

export default {
    path: '/mypage',
    component: Layout,
    children: [
        { path: '', component: Mypage },
        { path: 'apikey', component: ApiKey }
    ]
};

