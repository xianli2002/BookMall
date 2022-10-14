var vm = new Vue({
    el: '#app',
    data: {
        host: host,

        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_allow: false,
        error_name_message: '',
        error_phone_message: '',



        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: false,

    },
   
    methods: {
        
        // 检查用户名
        check_username: function () {
            var re = /^[a-zA-Z0-9_-]{5,20}$/;
            var re2 = /^[0-9]+$/;
            if (re.test(this.username) && !re2.test(this.username)) {
                this.error_name = false;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名且不能为纯数字';
                this.error_name = true;
            }
            // 检查重名
            if (this.error_name == false) {
                var url = this.host + '/usernames/' + this.username + '/count/';
                axios.defaults.withCredentials = true
                axios.get(url, {
                    responseType: 'json',
                    withCredentials:true,
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_cpwd: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },
        // 检查手机号
        check_phone: function () {
            var re = /^1[345789]\d{9}$/;

            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }
            if (this.error_phone == false) {
                var url = this.host + '/mobiles/' + this.mobile + '/count/';
                axios.get(url, {
                    responseType: 'json',
                     withCredentials:true,
                })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_phone_message = '手机号已存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },

        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        
        // 注册
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_allow();


            // 点击注册按钮之后, 发送请求 (下面的代码是通过请求体传参的)
            if (this.error_name == false && this.error_password == false && this.error_check_password == false
                && this.error_phone == false && this.error_allow == false) {
                axios.post(this.host + '/register/new/', {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    allow: this.allow
                }, {
                    responseType: 'json',
                    withCredentials:true,
                })
                    .then(response => {
                        if (response.data.code==0) {
                           location.href = 'index.html';
                        }
                        if (response.data.code == 400) {
                            alert(response.data.errmsg)
                        }
                    })
                    .catch(error => {
                        if (error.response.code == 400) {
                            if ('non_field_errors' in error) {
                                this.error_sms_code_message = error.response;
                            } else {
                                this.error_sms_code_message = '数据有误';
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error);
                        }
                    })
            }
        }
    }
});