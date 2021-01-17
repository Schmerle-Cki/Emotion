<template>
    <div id="message-board">
		<p v-if="showResult===true" style="font-weight: bold;font-size: 30px;">实验结束，感谢您的参与!</p>
        <el-container v-if="currentStateShowsPhoto()" style="height:100%; border: 1px solid #eee;">
			
            <el-main>
				<!--p>{{images[currentImageSrc][currentImgID]}}</p-->
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
            <el-footer v-if="showResult===false" style="text-align: center;">
                <button class="select-button" style="display: inline-block;margin-right: 15px;text-align: center;" v-on:click="nextPicture(1)">
                    <i class="el-icon-sunny" style="font-weight: bold; font-size: 15px;">  积极</i>
                </button>
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                <button class="select-button" v-on:click="nextPicture(2)" style="display: inline-block;margin-right: 15px;">
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                    <i class="el-icon-cloudy" style="font-weight: bold; font-size: 15px;">  中性</i>
                </button>
                <button class="select-button" v-on:click="nextPicture(3)" style="display: inline-block;margin-right: 15px;">
                <!--请修改这两行注释中间的代码完成"刷新"功能-->
                    <i class="el-icon-heavy-rain" style="font-weight: bold; font-size: 15px;">  消极</i>
                </button>
            </el-footer>
        </el-container>
		<el-container v-if="currentState===states.welcome">
			<el-main>
				<p class="main-font"  style="top:80%">欢迎参加实验</p>
				<p>您将看到一些真人面孔和卡通图片,</p>
				<p v-html="highLight('请回答面孔所表达的情绪类型,','情绪类型')"></p>
				<p v-html="highLight('并用鼠标点击对应的按钮,','鼠标点击')"></p>
				<p v-html="highLight('准确又快速地反应','准确又快速')"></p>
			</el-main>
			<el-footer style="text-align: center; font-size: 10px">
				<el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
				v-on:click="currentState+=1">
					<i class="el-icon-d-arrow-right">进入练习阶段</i>
				</el-button>				
			</el-footer>
		</el-container>
		<el-container v-if="currentState===states.enterC">
			<el-main>
				<p class="main-font" style="top:80%">卡通画</p>
				<p v-html="highLight('请准确又快速地判断卡通人脸的表情','准确又快速')"></p>
			</el-main>
			<el-footer style="text-align: center; font-size: 10px; font-weight: bold;font-family:'Times New Roman', Times, serif">
				<el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
				v-on:click="currentState+=1;currentImageSrc = 0;getCurrentImgSrc()">
					<i class="el-icon-d-arrow-right">继续</i>
				</el-button>				
			</el-footer>
		</el-container>
		<el-container v-if="currentState===states.enterP">
			<el-main>
				<p class="main-font" style="top:80%">真人</p>
				<p v-html="highLight('请准确又快速地判断真实人脸的表情','准确又快速')"></p>
			</el-main>
			<el-footer style="text-align: center; font-size: 10px">
				<el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
				v-on:click="currentState+=1;currentImageSrc = 1;getCurrentImgSrc()">
					<i class="el-icon-d-arrow-right">继续</i>
				</el-button>				
			</el-footer>
		</el-container>
		<el-container v-if="currentState===states.enterFormal">
			<el-main style="top:50%">
				<p class="main-font" style="top:80%">练习结束</p>
			</el-main>
			<el-footer style="text-align: center; font-size: 10px">
				<el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
				v-on:click="currentState+=1;currentImageSrc = 2;getCurrentImgSrc()">
					<i class="el-icon-d-arrow-right">开始实验</i>
				</el-button>				
			</el-footer>
		</el-container>
		<el-container v-if="currentState===states.end">
			<el-main style="top:50%">
				<p class="main-font" style="top:80%">实验结束，感谢您的参与</p>
			</el-main>			
		</el-container>
		<PostDialog
			v-bind:dialogVisible="basicInfo.dialogVisible && currentState===states.info"
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
				// user's basic info
                basicInfo:{
                  dialogVisible:true,
                  form:{
                      age:"",
                      sex:"",
                      user:""
                    }
                },
                imageSrc:require("../img/Y3F-20_happy.jpg"),
                images:[],			//currentDataSet used
				formalImages:[],
				cartoonImages:[],
				realmanImages:[],
				currentImageSrc:0,	//{0:cartoon,1:real,2:formal}
				labeledImg:[],		//{picName,Label} 1=happy 2=neutral 3=sad
				answers:[],			//{cartoonReal,userChoice,groundTruth,accurate}
                currentImgID:0,
                messageList: [],
				showResult:false,
				emotions:["none","happy","neutral","sad"],
				states:{info:0,welcome:1,enterC:2,cartoonPractice:3,enterP:4,realPractice:5,enterFormal:6,formal:7,end:8},
				currentState:0,
				highLight:function(val,keyword)
				{
					val = val+'';
					if(val.indexOf(keyword)!==-1&&keyword!==''){
						return val.replace(keyword,'<font color="#f00">' + keyword + '</font>');
					}
					else{
						return val;
					}
				}
            }
        },  
		created(){
			this.currentImgID = 0;
			this.showResult = false;
			const path = require('path');
			// Formal Ones
			const files = require.context('../img',true,/.jpg$/);			
			files.keys().forEach(item=>{			
				this.formalImages.push(path.basename(item,'.jpg'));				
			})
			// Cartoon Practice
			const files1 = require.context('../img/practiceCartoon',true,/.jpg$/);
			files1.keys().forEach(item=>{			
				this.cartoonImages.push(path.basename(item,'.jpg'));				
			})
			// RealMan Practice
			const files2 = require.context('../img/practiceReal',true,/.jpg$/);
			files2.keys().forEach(item=>{			
				this.realmanImages.push(path.basename(item,'.jpg'));				
			})
			
			// Disorder the pictures		
			this.formalImages.sort(randomNumber);
			
			// Label formal images
			for(var imgName of this.formalImages)
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
					if(imgName.indexOf("cartoon")!=-1)
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
		
			this.images.push(this.cartoonImages);
			this.images.push(this.realmanImages);
			this.images.push(this.formalImages);
		},
        methods:{            
			initialInfo(Block){
				this.basicInfo.dialogVisible = false;
				this.basicInfo.form.age = Block.age;
				this.basicInfo.form.sex = Block.sex;
				this.basicInfo.form.user = Block.user;
				
				let expireDays = 1000*60*60;
				this.$cookieStore.setCookie(Block.user,expireDays);
				this.currentState = this.states.welcome;
			},
            getCurrentImgSrc(){
				if(this.currentImageSrc === 0)
					this.imageSrc = require("../img/practiceCartoon/" + this.images[0][this.currentImgID] +".jpg");
				else if(this.currentImageSrc === 1)
					this.imageSrc = require("../img/practiceReal/" + this.images[1][this.currentImgID] +".jpg");
				else
					this.imageSrc = require("../img/" + this.images[2][this.currentImgID] +".jpg")			
            },
			nextPicture(emotion){
				// Just Practice
				if(this.currentImageSrc<2)
				{
					// next picture
					if(this.currentImgID < this.images[this.currentImageSrc].length-1)
					{
						this.currentImgID += 1;
						this.getCurrentImgSrc();
					}
					else{
						this.currentImgID = 0;
						this.currentState += 1;
					}
					return;
				}
				
				// Formal experiment:record user's answer
				var accurate = 0;
				var groundTruth = this.labeledImg[this.currentImgID].label;
				var kind = this.labeledImg[this.currentImgID].kind;
				if(emotion == groundTruth)
					accurate = 1;
				this.answers.push({"kind":kind,"user":emotion,"truth":groundTruth,"accurate":accurate});
					
				// next picture
				if(this.currentImgID < this.images[2].length-1)
				{
					this.currentImgID += 1;
					this.getCurrentImgSrc();
				}
				else{					
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
            },
			currentStateShowsPhoto(){
				return this.currentState === this.states.cartoonPractice
					||	this.currentState === this.states.realPractice
					||	this.currentState === this.states.formal;
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
		font-family:"times new roman";
		font-weight: bold;
    }
	
	.select-button{
		background-color: #c4dbff;
		color: #000000;	
		font-family:"times new roman";
		font-weight: bold;
		height: 70%;
		width: 100px;
		padding-right: 20px;
		border-radius: 20px;
		border-color: #e4fff6;
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
	.main-font {
		font-size: 30px;
		font-family:"times new roman";
		font-weight: bold;
		padding-top: 100px;
	}
</style>
