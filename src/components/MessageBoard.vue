<template>
    <div id="message-board">        		
        <el-container style="height:100%; border: 1px solid #eee;">
            <el-main>
                <img :src="imageSrc"/>
            </el-main>
            <el-footer style="text-align: center; font-size: 10px">
                <el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
                v-on:click="nextPicture(1)">
                    <i class="el-icon-sunny">积极</i>
                </el-button>
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                <el-button class="press-button" v-on:click="nextPicture(2)" style="display: inline-block;margin-right: 15px;">
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                    <i class="el-icon-cloudy" style="object-fit: fill">中性</i>
                </el-button>
                <el-button class="press-button" v-on:click="nextPicture(3)" style="display: inline-block;margin-right: 15px;">
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                    <i class="el-icon-heavy-rain" style="object-fit: fill">消极</i>
                </el-button>
            </el-footer>
        </el-container>
    </div>
</template>

<script type="text/javascript">
    export default {
        name: "MessageBoard",
        components: {
            //MessageList
            //PostDialog
        },
        // 请在下方设计自己的数据结构及函数来完成最终的留言板功能
        data(){
            return {                
                imageSrc:require("../assets/cuteIcon.png"),
                images:["cuteIcon","logo","加油"],
                currentImgID:0,
                messageList: []
            }
        },        
        methods:{
            visibleAndFill(){
                this.postDialog.dialogVisible = true
                this.state.username_valid=false
                var name = this.$cookieStore.getCookie()
                if(name)
                {
                    this.state.username = name
                    this.state.username_valid=true
                }
                else
                    this.state.username=""
            },
            getCurrentImgSrc(){
                this.imageSrc = require("../assets/" + this.images[this.currentImgID] +".png")
            },
			nextPicture(emotion){
				if(this.currentImgID < this.images.length-1&&0<emotion)
				{
					this.currentImgID += 1;										
				}
				else{
					this.currentImgID = 0;
				}
				this.getCurrentImgSrc();
			},
            appendBlock(Block){
                let expireDays = 1000*60*60
                this.$cookieStore.setCookie(Block.user,expireDays)

                this.alertDialog.dialogVisible=false

                this.$post({"title":Block.title,"content":Block.content}).then((response) =>{
                    this.alertDialog.dialogVisible=true
                    console.log(response)
                    this.refresh()
                })
                
                this.postDialog.dialogVisible=false
            },
            refresh(){
                this.$get().then((response)=>{
                    this.messageList=[]
                    for(var item in response.data)
                    {
                        var time = response.data[item].timestamp*1000
                        response.data[item].timestamp=time
                        this.messageList.push(response.data[item])
                    }
                    this.messageList.reverse()
                })
            }
        },
    }
</script>

<style scoped>
    #message-board{
        height: calc(100vh - 16px);
    }
    .message-tab{
        display: block;
        padding: 10px;
        text-align: left;
    }
    .press-button{
        background-color: #ffe199;
        color: #333;		
    }
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }
    .el-footer {
        background-color: #ffffff;
        color: #333;
        line-height: 60px;
    }
    .el-aside {
        color: #333;
    }
</style>
