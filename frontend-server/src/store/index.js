import { createStore } from 'vuex'
import createMultiTabState from 'vuex-multi-tab-state'
import axios from 'axios'
import auth from '../auth'
import router from '@/router'

export default createStore({
  state: {
    user: null,
    managers: [],
    product:null,
    products: [],
    products_based_on_rating: [],
    manager_products: [],
    products_standby: [],
    categories: [],
    categories_standby: [],
    cart: [],
    orders: [],
    reviews: [],
    requests: [],
    all_requests: [],
    notify:{show:false,role:''},
    flash:{show:false,color:'',message:''}
  },
  getters: {
    user: state=>{
      return state.user
    },
    product: state=>{
      return state.product
    },
    products: state=>{
      return state.products
    },
    products_home: state=>{
      return state.products.length<=10?state.products:state.products.slice(0,11)
    },
    products_based_on_rating:state=>{
      return state.products_based_on_rating.sort((curr,prev)=>prev.rating-curr.rating)
    },
    products_based_on_rating_home: state=>{
      if(state.products_based_on_rating.length<=10){
        console.log(state.products_based_on_rating);
        return state.products_based_on_rating
      }
      else{
        return state.products_based_on_rating.slice(0,11)
      }
    },
    manager_products: state=>{
      return state.manager_products
    },
    categories: state=>{
      return state.categories
    },
    cart: state=>{
      return state.cart
    },
    orders: state=>{
      return state.orders
    },
    managers: state=>{
      return state.managers
    },
    reviews: state=>{
      return state.reviews
    },
    requests: state=>{
      return state.requests
    },
    all_requests: state=>{
      return state.all_requests
    },
    notify: state=>{
      return state.notify
    },
    flash: state=>{
      return state.flash
    }
  },
  mutations: {
    user(state,user){
      state.user = user
    },
    managers(state,managers){
      state.managers = managers
    },
    get_product(state,{product,id}){
      if(id){
        state.product=state.products.find(product=>product.id == id)
        state.reviews=state.product.reviews
      }
      else{
        state.product=product
        state.reviews=product.reviews
      }
    },
    update_product(state,{product,id}){
      state.manager_products=state.manager_products.filter(product=>product.id!=id)
      state.products=state.products.filter(product=>product.id!=id)
      state.products_based_on_rating=state.products
      state.products.unshift(product)
      state.manager_products.unshift(product)
      state.products_based_on_rating=state.products
      state.products_standby=state.manager_products
    },
    delete_product(state,id){
      state.products=state.products.filter(product=>product.id!=id)
      state.manager_products=state.manager_products.filter(product=>product.id!=id)
      state.products_standby=state.manager_products
      state.products_based_on_rating=state.products
    },
    get_products(state,products){
      state.products = products
      state.products_based_on_rating = products
    },
    get_manager_products(state,products){
      state.manager_products = products
      state.products_standby = products
    },
    add_manager_product(state,product){
      state.manager_products.unshift(product)
      state.products.unshift(product)
      state.products_based_on_rating=state.products
      state.products_standby=state.manager_products
    },
    get_categories(state,categories){
      state.categories = categories
      state.categories_standby = categories
    },
    update_category(state,{category,id}){
      if(category){
        state.categories=state.categories.filter(category=>category.id!=id)
        state.categories_standby=state.categories
        state.categories.push(category)
        state.categories_standby=state.categories
      }
    },
    delete_category(state,id){
      let category=state.categories.find(category=>category.id==id)
      state.categories=state.categories.filter(category=>category.id!=id)
      state.categories_standby=state.categories
      state.products=state.products.filter(product=>product.category!=category.name)
      state.products_based_on_rating=state.products
      state.products_standby=state.products
    },
    add_category(state,category){
      state.categories.push(category)
      state.categories_standby=state.categories
    },
    product_search(state,value){
      if(value.length){
        state.manager_products=state.manager_products.filter(product=>{
        let product_name=product.name.toLowerCase()
        return product_name.includes(value.toLowerCase())
        })
      }
      else{
        state.manager_products=state.products_standby
      }
    },
    category_search(state,value){
      if(value.length){
        state.categories=state.categories.filter(category=>{
        let category_name=category.name.toLowerCase()
        return category_name.includes(value.toLowerCase())
        })
      }
      else{
        state.categories=state.categories_standby
      }
    },
    get_cart(state,products){
      state.cart=products
    },
    add_cart(state,product){
      state.cart.unshift(product)
    },
    update_cart(state,{id,quantity}){
      let product=state.cart.find(product=>product.id==id)
      state.cart=state.cart.filter(product=>product.id!=id)
      product.quantity=quantity
      state.cart.unshift(product)
    },
    delete_cart(state,id){
      state.cart=state.cart.filter(product=>product.id!=id)
    },
    place_order(state,orders){
      if(state.orders.length){
        orders.forEach(order=>{
          state.orders.push(order)
        })
      }
      orders.forEach(order=>{
        state.products.forEach(product=>{
          if(order.name==product.name){
            product.inventory-=order.quantity
          }
        })
      })
      state.cart=[]
    },
    add_review(state,{review,id}){
      state.reviews.push(review)
      let rating_count=0
      let reviews_size=state.reviews.length
      for(let [star,rating] of Object.entries(state.product.ratings)){
        if(star==review.rating){
          state.product.ratings[`${star}`]=rating+1
          rating+=1
        }
        rating_count+=rating*star
      }
      let rating=rating_count/reviews_size
      state.product.rating=Number.isInteger(rating)?rating.toString():rating.toFixed(2)
      if(state.products&&state.products.length){
        state.products=state.products.filter(product=>product.id!=id)
        state.products.push(state.product)
        state.products_based_on_rating=state.products
      }
    },
    delete_review(state,id){
      let user_id=state.user.id
      let review=state.reviews.find(review=>review.user_id==user_id)
      state.reviews=state.reviews.filter(review=>review.user_id!=user_id)
      state.product.reviews=state.reviews
      let rating_count=0
      let reviews_size=state.reviews.length?state.reviews.length:1
      for(let [star,rating] of Object.entries(state.product.ratings)){
        if(star==review.rating){
          state.product.ratings[`${star}`]=rating-1
          rating-=1
        }
        rating_count+=rating*star
      }
      let rating=rating_count/reviews_size
      state.product.rating=Number.isInteger(rating)?rating.toString():rating.toFixed(2)
      if(state.products&&state.products.length){
        state.products=state.products.filter(product=>product.id!=id)
        state.products.push(state.product)
      }
    },
    get_orders(state,orders){
      orders.forEach(order=>{
        state.orders.push(order)
      })
    },
    add_request(state,request){
      state.requests.push(request)
      state.all_requests.push(request)
    },
    get_all_requests(state,requests){
      state.all_requests=requests
    },
    request_approval(state,{id,status}){
      let request=state.all_requests.find(request=>request.id==id)
      state.all_requests=state.all_requests.filter(request=>request.id!=id)
      state.requests=state.requests.filter(request=>request.id!=id)
      request['status']=status
      state.requests.push(request)
    },
    get_manager_requests(state,requests){
      let id=state.user.id
      state.requests=requests.filter(request=>request.user_id==id)
    },
    delete_request(state,id){
      state.requests=state.requests.filter(request=>request.id!=id)
      state.all_requests=state.all_requests.filter(request=>request.id!=id)
    },
    get_managers(state,managers){
      state.managers=managers
    },
    manager_approval(state,id){
      state.managers=state.managers.filter(manager=>manager.id!=id)
    },
    notify(state,notify){
      state.notify=notify
    },
    flash(state,flash){
      state.flash=flash
    },
    sentiment(state,{user_id,product_id,like_count,dislike_count}){
      if(state.products&&state.products.length){
        let product=state.products.find(product=>product.id==product_id)
        product.reviews.forEach(review=>{
          if(review.user_id==user_id){
            review.dislikes=dislike_count
            review.likes=like_count
          }
        })
        state.product=product
        state.products=state.products.filter(product=>product.id!=product_id)
        state.products.push(state.product)
      }else{
        let product=state.product
        product.reviews.forEach(review=>{
          if(review.user_id==user_id){
            review.dislikes=dislike_count
            review.likes=like_count
          }
        })
        state.product=product
      }
    }
  },
  actions: {
    async sentiment({ commit },data){
      try {
        let response = await axios.post('review/sentiment',JSON.stringify(data))
        let sentimented = response.data.sentimented
        if(sentimented){
          let sentiment=response.data.sentiment
          commit('sentiment',{'user_id':data.user_id,'product_id':data.product_id,
          'like_count':sentiment.like_count,'dislike_count':sentiment.dislike_count})
        }
      } catch (error) {
        console.log(error)
      }
    },

    async get_managers({ commit }) {
      try {
        let response = await axios.get('user/admin/approval/managers')
        let managers = response.data.managers
        commit('get_managers', managers)
      } catch (error) {
        console.log(error)
      }
    },
  
    async manager_approval({ commit }, data) {
      try {
        let response = await axios.put('user/admin/manager/approval', JSON.stringify(data))
        let id = response.data.id
        commit('manager_approval', id)
      } catch (error) {
        console.log(error)
      }
    },
  
    async get_all_requests({ commit, state }) {
      if (!(state.all_requests && state.all_requests.length)) {
        try {
          let response = await axios.get('user/admin/request/all')
          let requests = response.data.requests
          commit('get_all_requests', requests)
        } catch (error) {
          console.log(error)
        }
      }
    },
  
    async request_approval({ commit }, data) {
      try {
        let response = await axios.put('user/admin/request/approval', JSON.stringify(data))
        commit('request_approval', data)
      } catch (error) {
        console.log(error)
      }
    },
  
    async get_manager_requests({ commit, state }) {
      if (!(state.requests && state.requests.length)) {
        try {
          let response = await axios.get('user/manager/request/all')
          let requests = response.data.requests
          commit('get_manager_requests', requests)
        } catch (error) {
          console.log(error)
        }
      }
    },
  
    async delete_manager_request({ commit }, id) {
      try {
        let response = await axios.delete(`/user/manager/request/delete/${id}`)
        let message = response.data.message
        if (response.data.deleted) {
          commit('delete_request', id)
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },
  
    async add_manager_request({ commit }, data) {
      try {
        let response = await axios.post('user/manager/request/add', JSON.stringify(data))
        let request = response.data.request
        let message = response.data.message
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
        commit('add_request', request)
      } catch (error) {
        console.log(error)
      }
    },
  
    async delete_user({ commit }, role) {
      try {
        let response = await axios.delete(`user/${role}/delete`)
        let message = response.data.message
        auth.removeToken()
        commit('user', null)
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
        router.push({ name: 'home' })
      } catch (error) {
        console.log(error)
      }
    },

    async verify_user({ commit }, verify_token) {
      try {
        let response = await axios.get(`user/verify/${verify_token}`)
        let { user, token, message } = response.data
        if (token) {
          auth.setToken(token)
          commit('user', user)
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async get_user({ commit, dispatch }) {
      try {
        let response = await axios.get('user/get')
        let user = response.data.user
        let role = user.role.toLowerCase()
        if (role == 'customer') {
          dispatch('get_cart')
        }
        if (user.role == 'admin') {
          dispatch('get_all_requests')
          dispatch('get_managers')
        }
        commit('user', user)
        return user
      } catch (error) {
        console.log(error)
      }
    },

    async user_signup({ commit }, { data, role }) {
      try {
        const response = await axios.post(`user/${role}/signup`, JSON.stringify(data))
        let message = response.data.message
        if (response.data.created) {
          commit('notify', { 'show': true, 'role': role })
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
          router.push({ name: 'home' })
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async user_forgot_password({ commit },data) {
      try {
        let response = await axios.post(`user/forgot_password`, JSON.stringify(data))
        let reset= response.data.reset
        let message = response.data.message
        if(reset){
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
          router.push({name: 'home'})
        }
        else{
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async user_signin({ commit, dispatch }, { data, role, next }) {
      try {
        const response = await axios.post(`user/${role}/signin`, JSON.stringify(data))
        let token = response.data.token
        let user = response.data.user
        let message = response.data.message
        if (token) {
          auth.setToken(token)
          commit('user', user)
          if (user.role == 'customer') {
            dispatch('get_cart')
          }
          if (user.role == 'admin') {
            dispatch('get_all_requests')
            dispatch('get_managers')
          }
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
          if(next){
            let route=decodeURIComponent(next)
            router.push({path: route})
          }
          else{
            router.push({name: 'home'})
          }
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async update_user({ commit }, { data, role }) {
      try {
        const response = await axios.put(`user/${role}/update`, JSON.stringify(data))
        let user = response.data.user
        let message = response.data.message
        commit('user', user)
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
      } catch (error) {
        console.log(error)
      }
    },

    async update_password_user({ commit }, data) {
      try {
        let response = await axios.put('user/customer/update_password', JSON.stringify(data))
        let message = response.data.message
        if (response.data.updated) {
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async signout_user({ state }) {
      state.user = null
      state.cart = []
      state.products_standby = []
      state.categories_standby = []
      state.manager_products = []
      state.requests = []
      state.all_requests = []
      state.orders = []
    },

    managers({ commit }, managers) {
      commit('managers', managers)
    },

    async get_product({ commit, state }, id) {
      try {
        if (!(state.products && state.products.length)) {
          let response = await axios.get(`product/${id}`)
          let product = response.data.product
          commit('get_product', { 'product': product, 'id': null })
        } else {
          commit('get_product', { 'product': null, 'id': id })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async update_product({ commit }, { data, id }) {
      try {
        let response = await axios.put(`product/update/${id}`, JSON.stringify(data))
        let message = response.data.message
        if (response.data.updated) {
          let product = response.data.product
          commit('update_product', { product, id })
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        } else {
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async delete_product({ commit }, id) {
      try {
        let response = await axios.delete(`product/delete/${id}`)
        let message = response.data.message
        commit('delete_product', id)
        if (response.data.deleted) {
          commit('flash', { 'show': true, 'color': 'green', 'message': message })
        } else {
          commit('flash', { 'show': true, 'color': 'red', 'message': message })
        }
      } catch (error) {
        console.log(error)
      }
    },

    async get_products({ commit,dispatch, state }) {
      try {
        if (!(state.products && state.products.length)) {
          let response = await axios.get('product/all')
          let products = response.data.products
          commit('get_products', products)
        }
      } catch (error) {
        console.log(error)
        setTimeout(() =>{
          dispatch('get_products')
        },5000)
      }
    },

    async get_manager_products({ commit, state }) {
      try {
        if (!(state.manager_products && state.manager_products.length)) {
          let response = await axios.get('user/manager/products')
          let products = response.data.products
          commit('get_manager_products', products)
        }
      } catch (error) {
        console.log(error)
      }
    },

  async add_manager_product({ commit, dispatch, state }, data) {
    try {
      let response = await axios.post('product/add', JSON.stringify(data))
      let product = response.data.product
      let message = response.data.message
      if (response.data.added) {
        if (!(state.products && state.products.length)) {
          dispatch('get_products')
          dispatch('get_manager_products')
        } else {
          commit('add_manager_product', product)
        }
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async get_categories({ commit,dispatch, state }) {
    try {
      if (!(state.categories && state.categories.length)) {
        let response = await axios.get('category/all')
        let categories = response.data.categories
        commit('get_categories', categories)
      }
    } catch (error) {
      console.log(error)
      setTimeout(() =>{
        dispatch('get_categories')
      },5000)
    }
  },

  async delete_category({ commit }, id) {
    try {
      let response = await axios.delete(`category/delete/${id}`)
      let message = response.data.message
      if (response.data.deleted) {
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
        commit('delete_category', id)
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async update_category({ commit }, { data, id }) {
    try {
      let response = await axios.put(`category/update/${id}`, JSON.stringify(data))
      let category = response.data.category
      let message = response.data.message
      if (response.data.updated) {
        commit('update_category', { category, id })
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
        router.push({ name: 'admin_category_section' })
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async add_category({ commit }, data) {
    try {
      let response = await axios.post('category/add', JSON.stringify(data))
      let category = response.data.category
      let message = response.data.message
      if (response.data.added) {
        commit('add_category', category)
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async get_cart({ commit, state }) {
    try {
      if (!(state.cart && state.cart.length)) {
        let response = await axios.get('cart/products')
        let products = response.data.products
        commit('get_cart', products)
      }
    } catch (error) {
      console.log(error)
    }
  },

  async add_cart({ commit }, { id, quantity }) {
    try {
      let response = await axios.post('cart/add', JSON.stringify({ id, quantity }))
      let updated = response.data.updated
      let added = response.data.added
      if (updated) {
        commit('update_cart', { id, quantity })
      }
      if (added) {
        let product = response.data.product
        commit('add_cart', product)
      }
    } catch (error) {
      console.log(error)
    }
  },

  async delete_cart({ commit }, id) {
    try {
      let response = await axios.delete(`cart/delete/${id}`)
      commit('delete_cart', id)
    } catch (error) {
      console.log(error)
    }
  },

  async place_order({ commit }) {
    try {
      let response = await axios.delete('cart/order')
      let orders = response.data.orders
      commit('place_order', orders)
    } catch (error) {
      console.log(error)
    }
  },

  async add_review({ commit }, { data, id }) {
    try {
      let response = await axios.post('review/add', JSON.stringify(data))
      let review = response.data.review
      let message = response.data.message
      if (response.data.added) {
        commit('add_review', { review, id })
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async delete_review({ commit }, id) {
    try {
      let response = await axios.delete(`review/delete/${id}`)
      let message = response.data.message
      if (response.data.deleted) {
        commit('delete_review', id)
        commit('flash', { 'show': true, 'color': 'green', 'message': message })
      } else {
        commit('flash', { 'show': true, 'color': 'red', 'message': message })
      }
    } catch (error) {
      console.log(error)
    }
  },

  async get_orders({ commit, state }) {
    try {
      if (!(state.orders && state.orders.length)) {
        let response = await axios.get('orders/all')
        let orders = response.data.orders
        commit('get_orders', orders)
      }
    } catch (error) {
      console.log(error)
    }
  }
}
//   plugins: [createMultiTabState({
//       statesPaths: ['all_requests','managers','products','categories']
//     })]
})
