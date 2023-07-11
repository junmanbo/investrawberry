import { Layout, Order } from '@/views/order';

export default {
    path: '/order',
    component: Layout,
    children: [
        { path: '', component: Order},
    ]
};
