import store from "./store"
export default {
    getToken(){
        return sessionStorage.getItem('token')
    },
    setToken(token){
        return sessionStorage.setItem('token',token)
    },
    removeToken(){
        return sessionStorage.removeItem('token')
    },
    isAuthenticated(){
        return this.getToken()?true:false
    },
    async isAuthourised(user,role){
        if(this.isAuthenticated()){
            let _user=!user?await store.dispatch('get_user'):user
            if(!role){return true}
            let _role=_user.role
            if(_role.toLowerCase()==role.toLowerCase()){
                return true
            }else{
                return false
            }
        }
        else{
            return !role?true:false
        }
    }
}