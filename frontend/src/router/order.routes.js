import { Layout, Order, Portfolio } from '@/views/order';

export default {
    path: '/order',
    component: Layout,
    children: [
        { path: '', component: Order},
        { path: 'portfolio', component: Portfolio},
    ]
};
