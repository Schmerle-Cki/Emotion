<template>
    <div id="message-board">        		
        <el-container style="height:100%; border: 1px solid #eee;">
            <el-main>
				<!--p>{{basicInfo.form.sex}}</p-->
                <img v-if="showResult===false" :src="imageSrc"/>
				<table style="position:absolute;left:25%;top:15%;" v-if="showResult===true" border="1px" width="600px">
					<tr>
						<td>图片类别</td>
						<td>用户判断</td>
						<td>实际情感</td>
						<td>是否正确</td>
					</tr>
					<tr v-for="res in answers" v-bind:key=res.user>
						<td>{{res.kind}}</td>
						<td>{{emotions[res.user]}}</td>
						<td>{{emotions[res.truth]}}</td>
						<td>{{res.accurate}}</td>
					</tr>
				</table>
            </el-main>
            <el-footer v-if="showResult===false" style="text-align: center; font-size: 10px">
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
		
		<PostDialog
			v-bind:dialogVisible="basicInfo.dialogVisible"
			v-bind:state="state"
			v-on:newMember="initialInfo"			
		/>
    </div>
</template>

<script type="text/javascript">
	import PostDialog from "@/components/PostDialog"
	var randomNumber = function(){
		return 0.5 - Math.random();
	}
    export default {
        name: "MessageBoard",
        components: {
            //MessageList
            PostDialog
        },
        // 请在下方设计自己的数据结构及函数来完成最终的留言板功能
        data(){
            return {
                basicInfo:{
                  dialogVisible:true,
                  form:{
                      age:"",
                      sex:"",
                      user:""
                    }
                },
                imageSrc:require("../img/Y3F-20_happy.jpg"),
                images:[],		//["cuteIcon","logo","加油"],
				labeledImg:[],	//{picName,Label} 1=happy 2=neutral 3=sad
				answers:[],		//{cartoonReal,userChoice,groundTruth,accurate}
                currentImgID:0,
                messageList: [],
				showResult:false,
				emotions:["none","happy","neutral","sad"]				
            }
        },  
		created(){
			this.currentImgID = 0;
			this.showResult = false;
			const path = require('path');
			const files = require.context('../img',true,/.jpg$/);
			console.log(files);
			files.keys().forEach(item=>{			
				this.images.push(path.basename(item,'.jpg'));				
			})
			
			// Disorder the pictures		
			this.images.sort(randomNumber);
			
			for(var imgName of this.images)
			{
				if(imgName.indexOf("happy")!=-1)
				{
					if(imgName.indexOf("cartoon")!=-1)
					{						
						this.labeledImg.push({"kind":"cartoon","name":imgName,"label":1});
					}
					else
						this.labeledImg.push({"kind":"realMan","name":imgName,"label":1});
				}
				else if(imgName.indexOf("neutral")!=-1)
				{
					if(imgName[imgName.length-1]==='n')
					{						
						this.labeledImg.push({"kind":"cartoon","name":imgName,"label":2});
					}
					else
						this.labeledImg.push({"kind":"realMan","name":imgName,"label":2});
				}
				else
				{
					if(imgName.indexOf("cartoon")!=-1)
					{						
						this.labeledImg.push({"kind":"cartoon","name":imgName,"label":3});
					}
					else
						this.labeledImg.push({"kind":"realMan","name":imgName,"label":3});
				}
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
			initialInfo(Block){
				this.basicInfo.dialogVisible = false;
				this.basicInfo.form.age = Block.age;
				this.basicInfo.form.sex = Block.sex;
				this.basicInfo.form.user = Block.user;
				
				let expireDays = 1000*60*60;
				this.$cookieStore.setCookie(Block.user,expireDays);
			},
            getCurrentImgSrc(){
                this.imageSrc = require("../img/" + this.images[this.currentImgID] +".jpg")				
            },
			nextPicture(emotion){
				// record user's answer
				var accurate = 0;
				var groundTruth = this.labeledImg[this.currentImgID].label;
				var kind = this.labeledImg[this.currentImgID].kind;
				if(emotion == groundTruth)
					accurate = 1;
				this.answers.push({"kind":kind,"user":emotion,"truth":groundTruth,"accurate":accurate});
					
				// next picture
				if(this.currentImgID < this.images.length-1)
				{
					this.currentImgID += 1;
					this.getCurrentImgSrc();
				}
				else{
					//this.currentImgID = 0;
					this.showResult = true;
				}
				
			},
            sendBack(){
				var form = this.basicInfo.form;
				this.$post({"age":form.age,"sex":form.sex,"name":form.user,"data":this.answers}).then((response) =>{
					//this.alertDialog.dialogVisible=true
					console.log(response)
					//this.refresh()
				})

                /*this.alertDialog.dialogVisible=false

                this.$post({"title":Block.title,"content":Block.content}).then((response) =>{
                    this.alertDialog.dialogVisible=true
                    console.log(response)
                    this.refresh()
                })
                
                this.postDialog.dialogVisible=false*/
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
