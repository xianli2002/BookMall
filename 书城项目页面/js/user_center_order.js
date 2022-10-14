var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        username: '',
        orders_list:[],
        if_order:1,
        
        
    },
    mounted: function () {
        // 给 username 赋值:
        this.username = getCookie('username');
        this.get_order();

    },
    methods: {
         // 退出登录按钮
         logoutfunc: function () {
            var url = this.host + '/logout/';
            axios.delete(url, {
                responseType: 'json',
                withCredentials:true,
            })
                .then(response => {
                    location.href = 'login.html';
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        get_order:function(){
            axios.get(this.host + '/orders/get/', {
                responseType: 'json',
                withCredentials:true,
            }) 
            .then(response => {
                console.log(response.data.code)
                if (response.data.code==0){
                    this.orders_list=response.data.orders;
                    this.if_order=1;
                }
                else
                    this.if_order=0
            })
            .catch(error => {
                console.log(error)
            });
        },
        
    }
})