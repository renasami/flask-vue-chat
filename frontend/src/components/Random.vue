<template height="100%">
  <div class="video-container">
    <div class="video-area">
        <video
        id="my-video"
        autoplay
        playsinline />
        <video
        id="other-video"
        autoplay
        playsinline />
    </div>
    <div class="btns">
    <p>Your Video ID: <span id="js-local-id">{{ peerId }}</span></p>
    <input type="text" placeholder="通話相手のID"  v-model="calltoid"><br>
      <button :class="isMuteAudio ? 'can' : 'disabled'" @click="muteAudio()">audio</button>
      <button :class="isMuteVideo ? 'can' : 'disabled'" @click="muteVideo()">video</button>
      <button @click="connect">connection</button>
      <button @click="close" id="close">close</button>
    </div>
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
    </div>
  </div>
</template>
<script>
import Peer from 'skyway-js';
import axios from 'axios'
import * as io from "socket.io-client";

export default {
  data () {
      return {
        videos: [],
        audios: [],
        selectedAudio: '',
        selectedVideo: '',
        localStream: null,
        isMuteAudio: false,
        isMuteVideo: false,
        skywayKey: 'c7a61801-29ab-4d90-8529-98760ec84aed',
        peerId:'',
        calltoid:'',
        message: [],
      }
    },
    async mounted () {
      await this.prepareAudioVideoDevice()
      await this.connectLocalCamera()
      this.peer = new Peer({key: this.skywayKey, debug: 3})
      this.peer.on('open', () => this.peerId = this.peer.id)
      const closeTrigger = document.getElementById('close');

      this.peer.on('call', mediaConnection => {
        mediaConnection.answer(this.localStream);
        mediaConnection.on('stream', async stream => {
          // Render remote stream for callee
          remoteVideo.srcObject = stream;
          //remoteVideo.playsInline = true;
          await remoteVideo.play().catch(console.error);
        });
        mediaConnection.once('close', () => {
          remoteVideo.srcObject.getTracks().forEach(track => track.stop());
          remoteVideo.srcObject = null;
        });

        closeTrigger.addEventListener('click', () => mediaConnection.close(true));
      });
    },

    destroyed() {
      this.disconnectLocalCamera()
    },

    methods: {
      prepareAudioVideoDevice () {
        navigator.mediaDevices.enumerateDevices()
          .then(deviceInfos => {
            // MediaDeviceInfo
            // - deviceId （デバイスID)
            // - kind 3type（audioinput, videoinput, audiooutput）
            // - label （名称）※ 取得できる場合と、できない場合がある
            // - groupId
            const audios = [{ text: '指定なし', value: '' }]
            const videos = [{ text: '指定なし', value: '' }]
            for (let i = 0; i < deviceInfos.length; i++) {
              const deviceInfo = deviceInfos[i]
              if (deviceInfo.kind === 'audioinput') {
                audios.push({
                  text: deviceInfo.label || `Microphone ${audios.length + 1}`,
                  value: deviceInfo.deviceId
                })
              } else if (deviceInfo.kind === 'videoinput') {
                videos.push({
                  text: deviceInfo.label || `Camera  ${videos.length + 1}`,
                  value: deviceInfo.deviceId
                })
              }
            }
            this.audios = audios
            this.videos = videos
          })
      },

      connectLocalCamera () {
        const constraints = {
          audio: this.selectedAudio ? { deviceId: { exact: this.selectedAudio } } : true,
          video: this.selectedVideo ? { deviceId: { exact: this.selectedVideo } } : true,
        }

        if (this.localStream) {
          this.localStream = null
        }

        navigator.mediaDevices.getUserMedia(constraints)
          .then(stream => {
            document.getElementById('my-video').srcObject = stream
            this.localStream = stream
          }).catch(error => {
            console.error('mediaDevice.getUserMedia() error:', error)
          })
      },

      muteAudio () {
        if (!this.localStream) return
        this.localStream.getAudioTracks()[0].enabled = !this.isMuteAudio
        this.isMuteAudio = !this.isMuteAudio
      },

      muteVideo () {
        if (!this.localStream) return
        if (!this.isMuteVideo) {
          // Mute
          this.localStream.getVideoTracks()[0].stop()
          this.localStream.removeTrack(this.localStream.getVideoTracks()[0])
          document.getElementById('my-video').srcObject = null
        } else {
          // Re-connect
          this.connectLocalCamera()
        }
        this.isMuteVideo = !this.isMuteVideo
      },

      disconnectLocalCamera () {
        if (!!this.localStream) {
          this.localStream.getTracks().forEach(track => track.stop())
          document.getElementById('my-video').srcObject = null
          this.localStream = null
        }
      },
      connect() {
        console.log('connect function')
        if (!this.peer.open) {
          return;
        }
        const remoteVideo = document.getElementById('other-video')
        const mediaConnection = this.peer.call(this.calltoid, this.localStream)
        mediaConnection.on('stream', async stream => {
          // Render remote stream for caller
          remoteVideo.srcObject = stream;
          //remoteVideo.playsInline = true;
          await remoteVideo.play().catch(console.error);
        });
        mediaConnection.once('close', () => {
          remoteVideo.srcObject.getTracks().forEach(track => track.stop());
          remoteVideo.srcObject = null;
        });
      },
      close(){
        console.log(this.localStream)
        mediaConnection.close(true)
      },
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
  video {
    width: 400px;
    height: 300px;
  }
  .btns {
    margin: 15px;
  }
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

