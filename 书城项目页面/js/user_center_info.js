var vm = new Vue({
    el: '#app',
    data: {
        host,
        username: '',
        mobile: '',
        address:'',
        histories: [],
    },
    mounted: function () {
        // 获取cookie中的用户名
        this.username = getCookie('username');

        // 获取个人信息:
        this.get_person_info();

        this.get_history();
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
        get_history:function(){
             // 添加下列代码, 发送请求, 获取用户的浏览记录信息:
            axios.get(this.host + '/browse_histories/', {
                    responseType: 'json',
                    withCredentials:true,
                })
                .then(response => {
                    this.histories = response.data.skus;
                    for(var i=0; i<this.histories.length; i++){
                      this.histories[i].url='/detail.html?book='+this.histories[i].id;
                    }
                })
                .catch(error => {
                    console.log(error)
                });
        },
        // 获取用户所有的资料
        get_person_info: function () {
            var url = this.host + '/info/';
            axios.get(url, {
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    if (response.data.code == 400) {
                        location.href = 'login.html'
                        return
                    }
                    this.username = response.data.info_data.username;
                    this.mobile = response.data.info_data.mobile;
                    this.address = response.data.address;
                    
                })
                .catch(error => {

                    location.href = 'login.html'
                })
        },
       
    }
});