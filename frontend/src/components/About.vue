<template>
    <div class="chat">
        <section>
            <div class="chat_list">
                <div v-for="m in message" :key="m.key">
                    <div>{{m.user_id}}さん「{{m.message}}」</div>
                </div>
            </div>
        </section>
        <section>
            <div class="my_chat">
                <input v-model="my_message" type="text" placeholder="あなたのチャット">
                <button @click="mySend">送信する</button>
            </div>
        </section>
        <button @click="o_s">os</button>
    </div>
</template>

<script>
import axios from 'axios'
import * as io from "socket.io-client";

export default {
    data(){
        return{
            message: [],
        }
    },
    name:"chat",
    methods:{
        mySend(){
            const socket = io('ws://localhost:5000/test')
            const path = 'http://localhost:5000/send_chat/'   
            var mainTal = {user_id:this.$store.state.username, message:this.my_message}
            socket.emit("message", JSON.stringify(mainTal));
            axios.post(path,mainTal)
            // .then((response) => {
            //     console.log(response.data)
            // })
            this.my_message = ''
        },
        getIp() {
          const path = 'http://localhost:5000/chat_api'
          axios.get(path)
          .then((response) => {
            var len = Object.keys(response.data).length
            console.log(response.data)
            console.log(this.$store.state.login)
            for(var n = 0 ; n < len ; n++ ){
                console.log(response.data)
                var cont = JSON.parse(response.data[n])
                console.log(cont["content"])
                //this.message.push({user_id:cont['user_id'],message:cont["content"]})
            }
        })
          .catch((e) => {
            console.log(e);
        });
        },
    },
    created() {
        const socket = io('ws://localhost:5000/test')
        const path = 'http://localhost:5000/chat_api'
        axios.get(path)
            .then((response) => {
            var len = Object.keys(response.data).length
            //console.log(response.data)
            console.log(this.$store.state.login)
            for(var n = 0 ; n < len ; n++ ){
                //console.log(response.data)
                var cont = JSON.parse(response.data[n])
                //console.log(cont["content"])
                this.message.push({user_id:cont['user_id'],message:cont["content"]})
            }
        })
        .catch((e) => {
            console.log(e);
        });
        socket.on('message', param => {
            param = JSON.parse(param)
            console.log(param["user_id"])
            console.log(param['message'])
            this.message.push({user_id:param['user_id'],message:param['message']})
        });
        
    },
    watch() {
        const unwatch = this.$store.watch(
        state => state.login,
        login => {
            console.log('login:', login)
            }
        )
    }
}
</script>
<style scoped>
    .chat {
        text-align: center;
        width: 60%;
        padding-left: 20%;
    }
    .chat_list {
        overflow: auto;
        height: 250px;
        border: solid;
    }
</style>

