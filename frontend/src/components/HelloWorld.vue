<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>{{ aler }}</p>
    <br>
    <input id="username" placeholder="input your username" type="text"  v-model="u_name"><br>
    <br>
    <input id="password" placeholder="input your password" type="text" v-model="u_pas"><br>
    <button @click="login">Log IN</button>
  </div>
</template>

<script>
import axios from 'axios'
import "../store/index.js"
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      aler: '',
      user:{
        name:'',
        pas:''
      }
    }
  },
  methods: {
    login(){
      console.log(this.$store.ip)
      const path = `http://localhost:5000/user_api/`
      if(this.u_name == undefined || this.u_pas == undefined){
        this.aler = "you must fill in the blanks two below"
        return
      }
      console.log(typeof this.user)
      this.user.name = this.u_name 
      this.user.pas = this.u_pas
      axios.post(path,this.user)
      .then((response) =>{
        console.log(response.data)
        console.log(typeof response.data)
        if(typeof response.data == "object"){
          this.$store.state.login = true
          console.log(this.$store.state.login)
          this.$store.state.username = this.user.name
          this.aler = ""
          this.msg = "こんにちは" + this.$store.state.username + "さん"
        }else if (typeof response.data == "string"){
          this.aler = response.data
        }
      })
      .catch((e) => {
            console.log(e);
        });
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
