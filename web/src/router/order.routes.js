import { Layout, Order, OrderForm } from '@/views/order';

export default {
    path: '/order',
    component: Layout,
    children: [
        { path: '', component: Order},
        { path: 'form', name: 'order-form', component: OrderForm},
    ]
};
