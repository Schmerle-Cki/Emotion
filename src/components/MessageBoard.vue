<template>
    <div id="message-board" style="background-color: #808080;">
        <preload-image v-if="loading === true" :imgUrlArr="imgUrls" @imgAllLoaded="loading=false"></preload-image>
        <el-container v-if="currentStateShowsPhoto()" style="height:100%; border: 1px solid #eee;">
            <el-main>
                <div v-if="showResult===false" class = "box">
                    <img v-if="imageDisplayState === 1" :src="imageSrc"/>				
                    <p v-if="showResult===false&&imageDisplayState === 0" style="font-weight: bold;font-size: 30px; margin: 135px;">+</p>
                </div>
                <p v-if="showResult===true" style="font-weight: bold;font-size: 30px;margin-top:20%; color: white;">实验结束，感谢您的参与!</p>
                <!--table style="position:absolute;left:25%;top:15%;" v-if="showResult===true" border="1px" width="600px">
                    <tr>
                        <td>图片类别</td>
                        <td>用户判断</td>
                        <td>实际情感</td>
                        <td>是否正确</td>
                    </tr>
                    <tr v-for="res in answers" v-bind:key=res.user>
                        <td>{{res.kind}}</td>
                        <td>{{res.user}}</td>
                        <td>{{res.truth}}</td>
                        <td>{{res.accurate}}</td>
                    </tr>
                </table-->
            </el-main>
            <el-footer v-if="showResult===false && imageDisplayState === 1" style="text-align: center;">
                <button class="select-button" style="display: inline-block;margin-right: 15px;text-align: center;" v-on:click="nextPicture(buttonEmotion[0].value)">
                    {{buttonEmotion[0].label}}
                </button>                
                <button class="select-button" style="display: inline-block;margin-right: 15px;text-align: center;" v-on:click="nextPicture(buttonEmotion[1].value)">
                    {{buttonEmotion[1].label}}
                </button>
                <button class="select-button" style="display: inline-block;margin-right: 15px;text-align: center;" v-on:click="nextPicture(buttonEmotion[2].value)">
                    {{buttonEmotion[2].label}}
                </button>
            </el-footer>
        </el-container>
        <el-container v-if="loading===false && currentState===states.welcome">
            <el-main>
                <p class="main-font"  style="top:80%">欢迎参加实验</p>
                <p style="color: white;">您将看到一些真人面孔和卡通图片,</p>
                <p style="color: white;" v-html="highLight('请回答面孔所表达的情绪类型,','情绪类型')"></p>
                <p style="color: white;" v-html="highLight('并用鼠标点击对应的按钮,','鼠标点击')"></p>
                <p style="color: white;" v-html="highLight('准确又快速地反应','准确又快速')"></p>
            </el-main>
            <el-footer style="text-align: center; font-size: 10px">
                <el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
                v-on:click="currentState+=1">
                    <i class="el-icon-d-arrow-right">进入练习阶段</i>
                </el-button>				
            </el-footer>
        </el-container>
        <el-container v-if="loading===false && currentState===states.enterC">
            <el-main>
                <p class="main-font" style="top:80%">卡通画</p>
                <p style="color: white;" v-html="highLight('请准确又快速地判断卡通人脸的表情','准确又快速')"></p>
            </el-main>
            <el-footer style="text-align: center; font-size: 10px; font-weight: bold;font-family:'Times New Roman', Times, serif">
                <el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
                v-on:click="currentState+=1;currentImageSrc = 0;getCurrentImgSrc()">
                    <i class="el-icon-d-arrow-right">继续</i>
                </el-button>				
            </el-footer>
        </el-container>
        <el-container v-if="loading===false && currentState===states.enterP">
            <el-main>
                <p class="main-font" style="top:80%">真人</p>
                <p style="color: white;" v-html="highLight('请准确又快速地判断真实人脸的表情','准确又快速')"></p>
            </el-main>
            <el-footer style="text-align: center; font-size: 10px">
                <el-button class="press-button" style="display: inline-block;margin-right: 15px;" 
                v-on:click="currentState+=1;currentImageSrc = 1;getCurrentImgSrc()">
                    <i class="el-icon-d-arrow-right">继续</i>
                </el-button>				
            </el-footer>
        </el-container>
        <el-container v-if="loading===false && currentState===states.enterFormal">
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
        <el-container v-if="loading===false && currentState===states.end" style="height:100%; border: 1px solid #eee;">			
            <el-header>
                <p>实验结束，感谢您的参与</p>
                <div class = "center main-font">
                    实验结束，感谢您的参与
                </div>
            </el-header>						
        </el-container>
        <PostDialog
            v-bind:dialogVisible="basicInfo.dialogVisible && currentState===states.info && loading === false"           
            v-on:newMember="initialInfo"			
        />
    </div>
</template>

<script type="text/javascript">
    import PostDialog from "@/components/PostDialog"
    import preloadImage from 'vue-preload-image'
    //import getImageList from '../utils/loadImage'
    
    //import { saveAs } from 'file-saver';
    var randomNumber = function(){
        return 0.5 - Math.random();
    }	
    export default {
        name: "MessageBoard",
        components: {
            //MessageList
            PostDialog,
            preloadImage
        },
        // 请在下方设计自己的数据结构及函数来完成最终的留言板功能
        data(){
            return {
                // user's basic info
                loading:true,
                imgUrls:this.preload(),
                url:process.env.VUE_APP_URL,
                basicInfo:{
                  dialogVisible:true,
                  form:{
                      age:"",
                      sex:"",
                      user:"",
                      handiness:""
                    }
                },
                imageSrc:require("../../static/img/formal/Y3F-20_happy.jpg"),
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
                // 状态机取值集合
                states:{info:0,welcome:1,enterC:2,cartoonPractice:3,enterP:4,realPractice:5,enterFormal:6,formal:7,end:8},
                // 状态机当前状态
                currentState:0,
                // 十字显示
                imageDisplayState:0,
                // 正式实验的图片
                CarMaterial:[],
                RelMaterial:[],
                // 按钮相对位置可切换
                buttonEmotion:[{label:"积极",value:1},{label:"中性",value:2},{label:"消极",value:3}],
                // 文本高亮
                highLight:function(val,keyword)
                {
                    val = val+'';
                    if(val.indexOf(keyword)!==-1&&keyword!==''){
                        return val.replace(keyword,'<font color="#f00">' + keyword + '</font>');
                    }
                    else{
                        return val.replace(keyword,'<font color="#ffffff">' + keyword + '</font>');
                    }
                }
            }
        },  
        created(){
            this.currentImgID = 0;
            this.showResult = false;		
            
            const path = require('path');
            // Formal Ones
            const files = require.context('../../static/img/formal',true,/.jpg$/);			
            files.keys().forEach(item=>{
                var name = path.basename(item,'.jpg');
                if(name.indexOf("cartoon")!==-1)
                    this.CarMaterial.push(name);
                else
                    this.RelMaterial.push(name);
                //this.formalImages.push(path.basename(item,'.jpg'));				
            })
            // Cartoon Practice
            const files1 = require.context('../../static/img/practiceCartoon',true,/.jpg$/);
            files1.keys().forEach(item=>{			
                this.cartoonImages.push(path.basename(item,'.jpg'));				
            })
            // RealMan Practice
            const files2 = require.context('../../static/img/practiceReal',true,/.jpg$/);
            files2.keys().forEach(item=>{			
                this.realmanImages.push(path.basename(item,'.jpg'));				
            })
            
            // Inner Disorder the pictures
            // TODO:change the outside order
            this.CarMaterial.sort(randomNumber);
            this.RelMaterial.sort(randomNumber);
            this.refresh();			
        },
        mounted:function(){
            //this.preload();
        },
        methods:{   
            preload(){
                const path = require('path');				
                let imgs = [];
                const files1 = require.context('../../static/img/practiceCartoon',true,/.jpg$/);
                files1.keys().forEach(item=>{			
                    imgs.push(path.basename(item,'.jpg'));				
                });
                // RealMan Practice
                const files2 = require.context('../../static/img/practiceReal',true,/.jpg$/);
                files2.keys().forEach(item=>{			
                    imgs.push(path.basename(item,'.jpg'));				
                });
                const files = require.context('../../static/img/formal',true,/.jpg$/);
                files.keys().forEach(item=>{
                    imgs.push(path.basename(item,'.jpg'));		
                });
                
                return imgs;
                
                /*for (let img of imgs) {
                    let image = new Image();
                    image.src = img;
                    image.onload = () => {
                        
                    };
                }*/
            },
            initialInfo(Block){
                this.basicInfo.dialogVisible = false;
                this.basicInfo.form.age = Block.age;
                this.basicInfo.form.sex = Block.sex;
                this.basicInfo.form.user = Block.user;
                this.basicInfo.form.handiness = Block.handiness;
                
                let expireDays = 1000*60*60;
                this.$cookieStore.setCookie(Block.user,expireDays);
                this.currentState = this.states.welcome;
            },
            getCurrentImgSrc(){
                this.timeOut = setTimeout(() => {
                    
                    console.log("ImageSrc:" + this.currentImageSrc);
                    
                    if(this.currentImageSrc === 0)
                        this.imageSrc = require("../../static/img/practiceCartoon/" + this.images[0][this.currentImgID] +".jpg");
                    else if(this.currentImageSrc === 1)
                        this.imageSrc = require("../../static/img/practiceReal/" + this.images[1][this.currentImgID] +".jpg");
                    else
                        this.imageSrc = require("../../static/img/formal/" + this.images[2][this.currentImgID] +".jpg")
                    this.imageDisplayState = 1;
                }, 500);							
            },
            nextPicture(emotion){
                this.imageDisplayState = 0;
                // this.buttonEmotion.sort(randomNumber);
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
                this.answers.push({"kind":kind,"user":this.emotions[emotion],"truth":this.emotions[groundTruth],"accurate":accurate});
                    
                // next picture
                if(this.currentImgID < this.images[2].length-1)
                {
                    this.currentImgID += 1;
                    this.getCurrentImgSrc();
                }
                else{					
                    this.showResult = true;
                    this.sendBack();
                }				
            },
            sendBack(){
                var form = this.basicInfo.form;
                this.storeData();
                this.$post({"gender":form.sex,"handiness":form.handiness,"age":form.age,"name":form.user,"data":this.answers})//.then((response) =>{
                    //this.alertDialog.dialogVisible=true
                    //console.log(response)
                    //this.refresh()
                //})
            },
            storeData(){			
                var FileSaver = require('file-saver');
                var date = new Date().toLocaleDateString();
                var form = this.basicInfo.form;
                var fullStr = "ID Date gender age handiness kind user truth accurate\n";
                for(var item of this.answers)
                {
                    fullStr += form.user+" " + date + " " + form.sex + " " + form.age + " " + form.handiness + " " + item.kind + " " + item.user + " " + item.truth + " " + item.accurate+"\n";
                }
                var blob = new Blob([fullStr],{type:"text/plain;charset=utf-8"});
                FileSaver.saveAs(blob,form.user + ".txt");				
            },
            refresh(){
                this.$get().then((response)=>{
                    var number = response.data[0].number;
                    console.log(number);
                    // 实验图片来源
                    if((number%2)!= 0)					
                        this.formalImages = this.CarMaterial.concat(this.RelMaterial);
                    else
                    {
                        this.formalImages = this.RelMaterial.concat(this.CarMaterial);
                    }
                        
                    // this.formalImages.sort(randomNumber);
                    // 按钮顺序
                    if((number%6) === 1)
                    {
                        this.buttonEmotion = [{label:"消极",value:3},{label:"中性",value:2},{label:"积极",value:1}];
                    }
                    else if((number%6) === 2)
                    {
                        this.buttonEmotion = [{label:"积极",value:1},{label:"中性",value:2},{label:"消极",value:3}];
                    }
                    else if((number%6) === 3)
                    {
                        this.buttonEmotion = [{label:"中性",value:2},{label:"积极",value:1},{label:"消极",value:3}];
                    }
                    else if((number%6) === 4)
                    {
                        this.buttonEmotion = [{label:"消极",value:3},{label:"积极",value:1},{label:"中性",value:2}];
                    }
                    else if((number%6) === 5)
                    {
                        this.buttonEmotion = [{label:"中性",value:2},{label:"消极",value:3},{label:"积极",value:1}];
                    }
                    else{
                        this.buttonEmotion = [{label:"积极",value:1},{label:"消极",value:3},{label:"中性",value:2}];
                    }
                    
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
                })
            },
            currentStateShowsPhoto(){
				if(this.loading === true)
					return false;
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
        font-family: "microsoft yahei";
        font-weight: bold;
        font-style: normal;
        font-size: 15px;
        height: 70%;
        width: 100px;		
        border-radius: 10px;
        border-color: #e4fff6;
    }
    
    .el-header {
        //background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }
    .el-footer {        
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
        padding-top: 100px ;
        color: white;
    }
    
    .box{
        position: absolute;
        width:300px;
        height:300px;
        left:50%;
        top:50%;
        margin-left:-150px ;
        margin-top: -150px;
    }	
    
    .button-font{		
        left:50%;
        top:50%;
        margin-left:-7px ;
        margin-top: -7px;
        font-size: 15px;
    }
    
    .logicColor {
        color: #808080;
    }
</style>
