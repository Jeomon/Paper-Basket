import { createRouter, createWebHistory } from 'vue-router'
import auth from '../auth'
import axios from 'axios'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ()=>import('../views/Home.vue'),
  },
  {
    path: '/product/',
    children: [
      {
        path: ':id',
        name: 'product',
        component: ()=>import('../views/product/ProductDetail.vue')
      },
      {
        path: 'all',
        name: 'products',
        component: ()=>import('../views/product/AllProducts.vue')
      },
      {
        path: 'search',
        name: 'product_search',
        component: ()=>import('../views/product/ProductSearchResult.vue')
      }
    ]
  },
  {
    path: '/category/search',
    name: 'category_search',
    component: ()=>import('../views/category/CategorySearchResult.vue')
  },
  {
    path: '/user/',
    children:[
      {
        path: 'verify/:token',
        name: 'user_verify',
        async beforeEnter(to,from,next){
          let verify_token=to.params.token
          store.dispatch('verify_user',verify_token)
          next({name: 'home'})
        }
      },
      {
        path: 'verify/reset_password/:token',
        name: 'user_verify_reset_password',
        async beforeEnter(to,from,next){
          try {
            let verify_token=to.params.token
            let response=await axios.get(`user/verify/reset_password/${verify_token}`)
            let {message,token}=response.data
            if(!token){
              store.commit('flash', { 'show': true, 'color': 'red', 'message': message })
              next({name:'home'})
            }
            else{
              next({name:'user_reset_password',params:{'verify_token':verify_token,'auth_token':token}})
            }
          } catch (error) {
            console.log(error)
          }
        }
      },
      {
        path: 'reset_password/:verify_token/:auth_token',
        name: 'user_reset_password',
        component: ()=>import('../views/user/ResetPassword.vue')
      },
      {
        path: 'customer',
        children: [
          {
            path: 'signup',
            component: ()=>import('../views/user/customer/SignUp.vue'),
            name: 'customer_signup',
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                next()
              }
            }
          },
          {
            path:'signin',
            component: ()=>import('../views/user/customer/SignIn.vue'),
            name: 'customer_signin',
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                if(!to.query.next){
                  to.query.next = encodeURIComponent(from.fullPath)
                  next(to)
                }
                else{
                  next()
                }
              }
            }
          },
          {
            path:'forgot_password',
            component: ()=>import('../views/user/ForgotPassword.vue'),
            name: 'customer_forgot_password',
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                next()
              }
            }
          },
          {
            path: "signout",
            name: "customer_signout",
            beforeEnter(to,from,next){
              auth.removeToken()
              store.dispatch('signout_user')
              next({name: 'home'})
            },
            meta: {
              auth: true,
              role: 'customer'
            }
          },
          {
            path: 'dashboard',
            component: ()=>import('../views/user/customer/Dashboard.vue'),
            children: [
              {
                path: 'update_profile',
                name: 'customer_update_profile',
                component: ()=>import('../views/user/customer/UpdateProfile.vue'),
                meta: {
                  auth: true,
                  role: 'customer'
                }
              },
              {
                path: 'change_password',
                name: 'customer_change_password',
                component: ()=>import('../views/user/customer/ChangePassword.vue'),
                meta: {
                  auth: true,
                  role: 'customer'
                }
              },
              {
                path: 'purchase_history',
                name: 'customer_purchase_history',
                component: ()=>import('../views/user/customer/PurchaseHistory.vue'),
                meta: {
                  auth: true,
                  role: 'customer'
                }
              },
              {
                path: 'delete_account',
                name: 'customer_delete_account',
                component: ()=>import('../views/user/customer/DeleteAccount.vue'),
                meta: {
                  auth: true,
                  role: 'customer'
                }
                
              }
            ],
            meta: {
              auth: true,
              roles: 'customer'
            }
          }
        ]
      },
      { 
        path: 'manager',
        children: [
          {
            path: 'signup',
            name: 'manager_signup',
            component: ()=>import('../views/user/manager/SignUp.vue'),
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                return next({name:'home'})
              }
              else{
                return next()
              }
            }
          },
          {
            path:'signin',
            name: 'manager_signin',
            component: ()=>import('../views/user/manager/SignIn.vue'),
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                if(!to.query.next){
                  to.query.next = encodeURIComponent(from.fullPath)
                  next(to)
                }
                else{
                  next()
                }
              }
            }
          },
          {
            path:'forgot_password',
            component: ()=>import('../views/user/ForgotPassword.vue'),
            name: 'manager_forgot_password',
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                next()
              }
            }
          },
          {
            path: "signout",
            name: "manager_signout",
            async beforeEnter(to,from,next){
              await axios.get('user/manager/signout')
              auth.removeToken()
              store.dispatch('signout_user')
              next({name: 'home'})
            },
            meta: {
              auth: true,
              role: 'manager'
            }
          },
          {
            path: 'dashboard',
            component: ()=>import('../views/user/manager/Dashboard.vue'),
            children: [
              {
                path: 'update_profile',
                name: 'manager_update_profile',
                component: ()=>import('../views/user/manager/UpdateProfile.vue'),
                meta: {
                  auth: true,
                  role: 'manager'
                }
              },
              {
                path: 'change_password',
                name: 'manager_change_password',
                component: ()=>import('../views/user/manager/ChangePassword.vue'),
                meta: {
                  auth: true,
                  role: 'manager'
                }
              },
              {
                path: 'product/',
                children: [
                  {
                    path: '',
                    component: ()=>import('../views/user/manager/ProductSection.vue'),
                    name:'manager_product_section',
                    meta: {
                      auth: true,
                      role: 'manager'
                    }
                  },
                  {
                    path: 'add',
                    component: ()=>import('../views/user/manager/AddProduct.vue'),
                    name:'manager_add_product',
                    meta: {
                      auth: true,
                      role: 'manager'
                    }
                  },
                  {
                    path: 'update/:id',
                    component: ()=>import('../views/user/manager/UpdateProduct.vue'),
                    name:'manager_update_product',
                    meta: {
                      auth: true,
                      role: 'manager'
                    }
                  }
                ],
                meta: {
                  auth: true,
                  role: 'manager'
                }
              },
              {
                path: 'trend_analysis',
                component: ()=>import('../views/user/manager/TrendAnalysis.vue'),
                name:'manager_trend_analysis',
                meta: {
                  auth: true,
                  role: 'manager'
                }
              },
              {
                path: 'request',
                children: [
                  {
                    path: '',
                    component: ()=>import('../views/user/manager/RequestSection.vue'),
                    name: 'manager_request_section',
                    meta: {
                      auth: true,
                      role: 'manager'
                    }
                  },
                  {
                    path: 'create',
                    component: ()=>import('../views/user/manager/CreateRequest.vue'),
                    name: 'manager_create_request',
                    meta: {
                      auth: true,
                      role: 'manager'
                    }
                  }
                ],
                meta: {
                  auth: true,
                  role: 'manager'
                }
              },
              {
                path: 'delete_account',
                name: 'manager_delete_account',
                component: ()=>import('../views/user/manager/DeleteAccount.vue'),
                meta: {
                  auth: true,
                  role: 'manager'
                }
              }
            ],
            meta: {
              auth: true,
              role: 'manager'
            }
          }
        ]
      },
      {
        path: 'admin',
        children: [
          {
            path: 'signin',
            name: 'admin_signin',
            component: ()=>import('../views/user/admin/SignIn.vue'),
            beforeEnter(to,from,next){
              if(auth.isAuthenticated()){
                next({name:'home'})
              }
              else{
                if(!to.query.next){
                  to.query.next = encodeURIComponent(from.fullPath)
                  next(to)
                }
                else{
                  next()
                }
              }
            }
          },
          {
            path: "signout",
            name: "admin_signout",
            beforeEnter(to,from,next){
              auth.removeToken()
              store.dispatch('signout_user')
              next({name: 'home'})
            },
            meta: {
              auth: true,
              role: 'admin'
            }
          },
          {
            path: 'dashboard',
            component: ()=>import('../views/user/admin/Dashboard.vue'),
            children: [
              {
                path: 'update_profile',
                name: 'admin_update_profile',
                component: ()=>import('../views/user/admin/UpdateProfile.vue'),
                meta: {
                  auth: true,
                  role: 'admin'
                }
              },
              {
                path: 'change_password',
                name: 'admin_change_password',
                component: ()=>import('../views/user/admin/ChangePassword.vue'),
                meta: {
                  auth: true,
                  role: 'admin'
                }
              },
              {
                path: 'category_approval',
                name: 'admin_category_approval',
                component: ()=>import('../views/user/admin/CategoryApproval.vue'),
                meta: {
                  auth: true,
                  role: 'admin'
                }
              },
              {
                path: 'manager_approval',
                name: 'admin_manager_approval',
                component: ()=>import('../views/user/admin/ManagerApproval.vue'),
                meta: {
                  auth: true,
                  role: 'admin'
                }
              },
              {
                path: 'category/',
                children: [
                  {
                    path: '',
                    name: 'admin_category_section',
                    component: ()=>import('../views/user/admin/CategorySection.vue'),
                    meta: {
                      auth: true,
                      role: 'admin'
                    }
                  },
                  {
                    path: 'add',
                    component: ()=>import('../views/user/admin/AddCategory.vue'),
                    name:'admin_add_category',
                    meta: {
                      auth: true,
                      role: 'admin'
                    }
                  },
                  {
                    path: 'update/:id',
                    component: ()=>import('../views/user/admin/UpdateCategory.vue'),
                    name:'admin_update_category',
                    meta: {
                      auth: true,
                      role: 'admin'
                    }
                  }
                ]
              }
            ],
            meta: {
              auth: true,
              role: 'admin'
            }
          }
        ]
      }
    ]
  },
  {
    path: '/:catchAll(.*)',
    name: '404_error',
    component: () =>import('../views/error/PageNotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async(to,from,next)=>{
  if(to.matched.some(record=>record.meta.auth)&&!auth.isAuthenticated()){
    let role=to.path.split('/')[2]
    let message="Sign in required"
    let path=encodeURIComponent(window.location.pathname)
    store.commit('flash',{'show': true,color:'red','message':message})
    next({name: `${role}_signin`,query:{next:path}})
  }
  else if(auth.isAuthenticated() && !store.state.user){
    let user=null
    let access=await auth.isAuthourised(user,to.meta.role)
    if(access){
      next()
    }
    else{
      let message="Access denied"
      store.commit('flash',{'show': true,color:'red','message':message})
      next({name: 'home'})
    }
  }
  else{
    let user=store.state.user
    let access=await auth.isAuthourised(user,to.meta.role)
    if(access){
      next()
    }
    else{
      let message="Access denied"
      store.commit('flash',{'show': true,color:'red','message':message})
      next({name: 'home'})
    }
  }
})

export default router
