import { Layout, Balance } from '@/views/balance';

export default {
    path: '/balance',
    component: Layout,
    children: [
        { path: '', component: Balance }
    ]
};

