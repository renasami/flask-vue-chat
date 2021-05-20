<template>
  <div id="app">
      <Controll />
      <img src="./assets/logo.png">
      <br>
      <router-view/>
      <Logout id="foot"/>
  </div>
</template>
<script>
import Controll from "@/components/Controll"
import Logout from "@/components/Logout"
import * as io from "socket.io-client";

export default {
  name: 'App',
  components:{
    Controll,
    Logout
  },
  created() {
        const unwatch = this.$store.watch(
        state => state.login,
        login => {
            console.log('login:', login)
          },
        )
        const unwatch2 = this.$store.watch(
        state => state.username,
        username => {
            console.log('username:', username)
          },
        )
  },
  mounted() {
    var socket = io('ws://localhost:5000/ip')
    socket.on("connect",function(){
      console.log("socket connected");
      socket.emit("ip",'need ip addr');
    });
    socket.on('ip',param => {
      this.$store.ip = param
    })

  },

}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  min-height: 100vh;
  position: relative;/*←相対位置*/
  padding-bottom: 120px;/*←footerの高さ*/
  box-sizing: border-box;/*←全て含めてmin-height:100vhに*/
  
}
#foot{
  width: 100%;
  background-color: #89c7de;
  color: #fff;
  text-align: center;
  padding: 30px 0;
  position: absolute;/*←絶対位置*/
  bottom: 0; /*下に固定*/
}
</style>
