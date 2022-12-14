var vm = new Vue({
    el: '#app',
    data: {
        host,
        f1_tab: 1, // 1F 标签页控制
        f2_tab: 1, // 2F 标签页控制
        f3_tab: 1, // 3F 标签页控制
        cart_total_count: 0, // 购物车总数量
        carts: [], // 购物车数据,
        A:{},
        B:{},
        C:{},
        username:'',
        content_category:{},
        goods_on_index:{},
    },
    mounted(){
        // 获取购物车数据
        this.get_cart();

         // 获取cookie中的用户名
    	this.username = getCookie('username');
        this.get_category_data();
        this.get_goods_on_index_data();

    },
    methods: {
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
        get_goods_on_index_data:function(){
            var url = this.host + '/goods_on_index/';
            axios.get(url, {
                responseType: 'json',
                withCredentials:true,
            })
                .then(response => {
                    this.goods_on_index = response.data.goods_on_index;
                    this.A = response.data.goods_on_index.A;
                    this.B = response.data.goods_on_index.B;
                    this.C = response.data.goods_on_index.C;
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
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
        // 获取购物车数据
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

    }
});










// $(function(){
//     // 楼层选项卡
// 	var $tab = $('.subtitle a');
// 	var $content = $('.goods_list_con .goods_list');
//
// 	$tab.click(function(){
// 		var $index = $tab.index($(this));
// 		$(this).addClass('active').siblings().removeClass('active');
// 		$content.eq($index).addClass('goods_list_show').siblings().removeClass('goods_list_show');
// 	});
//
// 	// 获取并展示购物车数据
// 	get_cart();
// });