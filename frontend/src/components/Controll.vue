<template>
    <header>
        <div class="header__flex">
        <h1 >
            <router-link to="/"><a>app</a></router-link> 
        </h1>
        <nav>
            <ul v-if="isLogin">
                <li>{{ userName }}</li>
                <router-link to="/" tag="li"><a>Home</a></router-link> 
                <router-link to="/random" tag="li"><a>Chat</a></router-link>
                <!-- <router-link to="/chat">chat</router-link> -->
            </ul>
            <ul v-else>
              <li>{{ userName }}</li>
              <li><a>Home</a></li>
              <li><a>Chat</a></li>
                <!-- <router-link to="/chat">chat</router-link> -->
            </ul>
        </nav>
        </div>
    </header>
</template>
<script>
export default {
    name: 'Controll',
    //props:['name'],
    data() {
      return {
        userName: '',
        isLogin: false
      }
    },
    methods: {
      must(){
        this.userName = "you must login at first"
      }
    },
    created() {
        const unwatch2 = this.$store.watch(
        state => state.username,
        username => {
            this.userName = username
            if(this.userName == ""){
              this.isLogin = false
            }else{
              this.isLogin = true
            }
            console.log(this.isLogin)
          },
        )
    },
}
</script>
<style scoped>
 * {
 margin: 0;
 padding: 0; 
 color: #000;
 text-decoration: none;
 background-color: aqua
 }
ul {
  list-style:none;
}
div {
  padding: 0 30px;
}
.header__flex {
  display: flex;
  height:60px;
  align-items: center;
}
.header__flex nav {
  margin-left: auto;
}
.header__flex ul {
  display: flex;
}
.header__flex ul li {
  margin-left: 20px;
}
</style>