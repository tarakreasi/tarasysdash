import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'dashboard',
            component: () => import('../views/DashboardView.vue')
        },
        {
            path: '/deployments',
            name: 'deployments',
            component: () => import('../views/DeploymentsView.vue')
        },
        {
            path: '/infrastructure',
            name: 'infrastructure',
            component: () => import('../views/InfrastructureView.vue')
        },
        {
            path: '/security',
            name: 'security',
            component: () => import('../views/SecurityView.vue')
        }
    ]
})

export default router
