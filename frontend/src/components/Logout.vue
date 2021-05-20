<template>
    <div id="wrapper">
        <footer>
            <router-link to="/" @click.native="logOut"><button>LogOut</button></router-link>
        </footer>
    </div>
</template>
<script>
export default {
    name: "LogOut",
    methods: {
        logOut(){
            console.log("logout")
            this.$store.state.login = false
            this.$store.state.username = ""
            console.log(this.$store.state.login)
            console.log(this.$store.state.username)
            
        },
    },
    // created() {
    //     const unwatch = this.$store.watch(
    //     state => state.login,
    //     login => {
    //         console.log('login:', login)
    //         }
    //     )
    // }   
}
</script>
<style scoped>
#wrapper{
    min-height: 100%;
    position: relative;/*←相対位置*/
    padding-bottom: 120px;/*←footerの高さ*/
    bottom: 0;
}
footer{
    width: 100%;
    background-color: #89c7de;
    color: #fff;
    text-align: center;
    padding: 30px 0;
    position: absolute;/*←絶対位置*/
    bottom: 0; /*下に固定*/
}
</style>