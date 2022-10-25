var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host,
        username: '',
        token: sessionStorage.token || localStorage.token,
        tab_content: {
            detail: true,
            pack: false,
            comment: false,
            service: false
        },
        sku:{},
        sku_id: '',
        sku_count: 1,
        sku_price: price,
        cart_total_count: 0, // 购物车总数量
        carts: [], // 购物车数据
        hots: [], // 热销商品
        cat: cat, // 商品类别
        comment:[], // 评论信息
        content_category:{},
        score_classes: {
            1: 'stars_one',
            2: 'stars_two',
            3: 'stars_three',
            4: 'stars_four',
            5: 'stars_five',
        }
    },
    computed: {
        sku_amount: function(){
            return (this.sku_price * this.sku_count).toFixed(2);
        }
    },
    mounted: function(){
        this.username=getCookie('username');
        this.get_sku_id();

        axios.post(this.host+'/good_detail/', {
            sku_id: this.sku_id
        },{
                responseType: 'json',
                withCredentials:true,
            })
            .then(response=>{
                this.sku=response.good_detail

            })
            .catch(error=>{
                console.log(error)
            })
        this.get_category_data();    
        this.get_cart();
        this.get_hot_goods();
        this.get_comments();
        this.detail_visit();
    },
    methods: {
         // 退出登录按钮
         get_category_data:function(){
            var url = this.host + '/content_category/';
            axios.get(url, {
                responseType: 'json',
                withCredentials:true,
            })
                .then(response => {
                    this.content_category = response.data.content_category;
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
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
        // 控制页面标签页展示
        on_tab_content: function(name){
            this.tab_content = {
                detail: false,
                pack: false,
                comment: false,
                service: false
            };
            this.tab_content[name] = true;
        },
        // 从路径中提取sku_id
        get_sku_id: function(){
            var re = /.*book=(.*)/;
            this.sku_id = document.location.pathname.match(re)[0];
        },
        // 减小数值
        on_minus: function(){
            if (this.sku_count > 1) {
                this.sku_count--;
            }
        },
        // 增加数值
        on_addition: function(){
            if (this.sku_count < 20) {
                this.sku_count++;
            }
        },
         // 添加购物车
        add_cart: function(){
            var url = this.host + '/carts/'
            axios.post(url, {
                    sku_id: parseInt(this.sku_id),
                    count: this.sku_count
                }, {
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    alert('添加购物车成功');
                    this.get_cart();
                })
                .catch(error => {
                    console.log(error);
                })
        },
       get_cart(){
        let url = this.host + '/carts/';
        axios.get(url, {
            responseType: 'json',
            withCredentials:true,
        })
            .then(response => {
                this.carts = response.data.cart_skus;
                this.cart_total_count = 0;
                for(let i=0;i<this.carts.length;i++){
                    if (this.carts[i].name.length>25){
                        this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                    }
                    this.cart_total_count += this.carts[i].count;
                }
            })
            .catch(error => {
                console.log(error);
            })
    },
        // 获取热销商品数据
        get_hot_goods: function(){

        },
        // 获取商品评价信息
        get_comments: function(){

        }
    }
});